import json, re, bcrypt, jwt, boto3, uuid, logging
import datetime 

from datetime import datetime

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Q, Sum, Count

from projects.models        import Project, Patron, Option, Category, Tag, Comment

from users.models            import User
from users.utils             import login_decorator
from my_settings             import ACCESS_KEY_ID, BUCKET_NAME, SECRET_ACCESS_KEY


class CloudStorage:
    def __init__(self, ACCESS_KEY_ID, SECRET_ACCESS_KEY, BUCKET_NAME):
        self.ACCESS_KEY_ID = ACCESS_KEY_ID
        self.SECRET_ACCESS_KEY = SECRET_ACCESS_KEY
        self.BUCKET_NAME = BUCKET_NAME
        self.client = boto3.client(
                's3',
                aws_access_key_id     = ACCESS_KEY_ID,
                aws_secret_access_key = SECRET_ACCESS_KEY,
            )
        self.resource = boto3.resource(
                's3',
                aws_access_key_id     = ACCESS_KEY_ID,
                aws_secret_access_key = SECRET_ACCESS_KEY,
            )
        
    def upload_file(self, file):
        unique_id = str(uuid.uuid4()) + file.name
        return self.client.upload_fileobj(
            file,
            self.BUCKET_NAME,
            unique_id,
            ExtraArgs = {
                'ContentType' : file.content_type
            }
        )

    def delete_file(self, main_image_url, project_id):
        main_image_url = Project.objects.get(id=project_id).main_image_url
        bucket = self.resource.Bucket(name=BUCKET_NAME)
        # bucket.delete_object(Key = main_image_url)
        bucket.Object(key = main_image_url).delete()

class ProjectUpload(View):
    @login_decorator
    def post(self, request):
        cloud_storage = CloudStorage(ACCESS_KEY_ID, SECRET_ACCESS_KEY, BUCKET_NAME)
        try:
            data = request.POST
            file = request.FILES.get('image')

            if file:
                cloud_storage.upload_file(file)
                unique_id = str(uuid.uuid4()) + file.name

            if not file:
                return JsonResponse({'MESSAGE' : 'IMAGE_EMPTY'}, status=400)

            Project.objects.create(
                    name           = data.get('name'),
                    user_id        = request.user.id,
                    aim_amount     = data.get('aim_amount'),
                    description    = data.get('description'),
                    end_date       = data.get('end_date')[0:4]+'-'+data.get('end_date')[5:7]+'-'+data.get('end_date')[8:10],
                    category_id    = data.get('category_id'),
                    main_image_url = 'https://humble.s3.ap-northeast-2.amazonaws.com/' + unique_id
                    )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE':'ERROR_INPUT_VALUE'}, status=404)

class ProjectModify(View):
    @login_decorator
    def post(self, request, project_id):
        try:
            data = request.POST

            if not Project.objects.filter(id=project_id, user_id=request.user.id).exists():
                return JsonResponse({'MESSAGE':'NOT_EXISTS'}, status=400)
            
            # file = request.FILES.get('image')

            # if file:
            #     cloud_storage.delete_file(file, main_image_url)
            #     file = request.FILES.get('image')
            #     main_image_url = 'https://humble.s3.ap-northeast-2.amazonaws.com/' + unique_id
                
            # if not file:
            #     main_image_url = Project.objects.get(id=project_id).main_image_url
            
            print(data.get('end_date'))

            Project.objects.filter(id=project_id, user_id=request.user.id).update(
                    name           = data.get('name'),
                    user_id        = request.user.id,
                    aim_amount     = data.get('aim_amount'),
                    description    = data.get('description'),
                    end_date       = data.get('end_date')[0:4]+'-'+data.get('end_date')[5:7]+'-'+data.get('end_date')[8:10],
                    category_id    = data.get('category_id'),
                    # main_image_url = main_image_url
                    )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE':'ERROR_INPUT_VALUE'}, status=404)

    @login_decorator
    def delete(self, request, project_id):
        cloud_storage = CloudStorage(ACCESS_KEY_ID, SECRET_ACCESS_KEY, BUCKET_NAME)
        user = request.user

        if not Project.objects.filter(id=project_id, user_id=user.id).exists():
            return JsonResponse({'MESSAGE':'NOT_EXISTS'}, status=400)
        
        # main_image_url = Project.objects.get(id=project_id).main_image_url        
        # cloud_storage.delete_file(main_image_url, project_id)

        Project.objects.get(id=project_id, user_id=user.id).delete()

        return JsonResponse({"MESSAGE": 'SUCCESS'}, status=204)


class ProjectListView(View):
    def get(self, request):
        today = datetime.now()
        category_id = request.GET.get("categoryId")

        q = Q()

        if category_id:
            q &= Q(category_id = category_id)
        
        limit        = int(request.GET.get('limit', 12))
        offset       = int(request.GET.get('offset', 0))

        projects = Project.objects.annotate(total=Sum('patron__total_amount'), count=Count('patron')).prefetch_related('tag').select_related('user', 'category').filter(q).order_by('created_at')[offset:offset+limit]

        projects = [{
                'tag'             : [{'id':tag.id, 'name':tag.tag} for tag in project.tag.all()],
                'name'            : project.name,
                'id'              : project.id,
                'user_id'         : project.user_id,
                'user'            : project.user.nickname,
                'remaining_time'  : (project.end_date.replace(tzinfo=None) - today).days,
                'main_image_url'  : project.main_image_url,
                'category_name'   : project.category.name,
                "aim_amount"      : project.aim_amount,
                'payment_date'    : project.end_date.strftime("%Y년 %m월 %d일"),
                'collected_amount': project.total,
                'percentage' : '%.f%%'%(project.total/project.aim_amount*100) if project.total else '0%',
                "created_at"      : project.created_at,
                "end_date"        : project.end_date, 
                "description"     : project.description
            } for project in projects]
            
        return JsonResponse({"project" : projects}, status=200)

class SearchView(View):
    def get(self, request):
        search = request.GET.get('search', None)
        projects = Project.objects.none()

        if Category.objects.filter(name__contains=search).exists():
            projects = Project.objects.filter(category__name__contains=search)

        if Tag.objects.filter(tag__contains=search).exists():
            projects = projects.union(Project.objects.filter(tag__tag__contains=search))

        if Project.objects.filter(name__contains=search).exists():
            projects = projects.union(Project.objects.filter(name__contains=search))

        if Project.objects.filter(description__contains=search).exists():
            projects = projects.union(Project.objects.filter(description__contains=search))

        results = [{
                    "id"             : project.id,
                    "category_id"    : project.category_id,
                    "user_id"        : project.user_id,
                    "user_name"      : project.user.nickname,
                    "name"           : project.name,
                    "image"          : project.main_image_url,
                    "aim_amount"     : project.aim_amount,
                    "created_at"     : project.created_at,
                    "end_date"       : project.end_date, 
                    "description"    : project.description,
            } for project in projects]

        return JsonResponse({'MESSAGE':results}, status=200)

class CommentView(View):
    @login_decorator
    def post(self, request, project_id):
        try:
            if Comment.objects.filter(project_id=project_id, user_id=5).exists():
                return JsonResponse({'MESSAGE' : 'COMMENT_ALREADY_EXIST'}, status=400)

            data        = json.loads(request.body)
            description = data['description']

            if not description:
                return JsonResponse({'MESSAGE' : 'EMPTY_CONTENT'}, status=400)

            Comment.objects.create(
                user        = request.user,
                project_id  = project_id,
                description = data['description']
            )
            return JsonResponse({'MESSAGE' : 'COMMENT_CREATED'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

    @login_decorator
    def delete(self, request, project_id):
        comment = Comment.objects.filter(project_id=project_id, user_id=5)
        if not comment.exists():
            return JsonResponse({'MESSAGE' : 'COMMENT_DOES_NOT_EXIST'}, status=400)

        comment.delete()
        return JsonResponse({'MESSAGE' : 'COMMENT_DELETED'}, status=204)

    def get(self, request, project_id):
        comments = Comment.objects.filter(project_id=project_id).select_related('user').order_by('-id')

        comment_list = [{   
                'user_id'           : comment.user_id,
                'nickname'          : comment.user.nickname,
                'description'       : comment.description,
                } for comment in comments
            ]
        return JsonResponse({'comments':comment_list}, status=200)

class ProjectView(View):
    def get(self, request, project_id):  
        today = datetime.now()

        if not Project.objects.filter(id=project_id).exists():
            return JsonResponse({'message': 'PROJECT_NOT_EXIST'}, status=404)

        project = Project.objects.annotate(total=Sum('patron__total_amount'), count=Count('patron')).prefetch_related('tag').select_related('user').get(id=project_id) 

        project_information = {
            'tag'               : [{'id':tag.id, 'name':tag.tag} for tag in project.tag.all()],
            'name'              : project.name,
            'user'              : project.user.nickname,
            'remaining_time'    : (project.end_date.replace(tzinfo=None) - today).days,
            'number_of_sponsors': project.count,
            'main_image_url'    : project.main_image_url,
            'aim_amount'        : project.aim_amount,
            'payment_date'      : project.end_date.strftime("%Y년 %m월 %d일"),
            'collected_amount'  : project.total if project.total else 0,
            'percentage'        : '%.f%%'%(project.total/project.aim_amount*100) if project.total else '0%',
        }

        return JsonResponse({'project_information':project_information}, status=200)

class ProjectOptionView(View):
    @login_decorator
    def post(self, request, project_id):
        try:
            data = json.loads(request.body)
            user = request.user

            Patron.objects.create(
                project_id   = project_id,
                user_id      = user.id,
                option_id    = data['option_id'],
                total_amount = data['total_amount']
            )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

    def get(self, request, project_id):
        options = Option.objects.filter(project_id=project_id)

        option = [{
            'id'            : option.id,
            'option_name'   : option.name,
            'option_amount' : int(option.amount)
        } for option in options]

        return JsonResponse({'option':option}, status=200)
            
    @login_decorator
    def post(self, request):
        cloud_storage = CloudStorage(ACCESS_KEY_ID, SECRET_ACCESS_KEY, BUCKET_NAME)
        try:
            data = request.POST
            file = request.FILES.get('image')

            if not file:
                return JsonResponse({'MESSAGE' : 'IMAGE_EMPTY'}, status=400)
            
            if file:
                cloud_storage.upload_file(file)
                unique_id = str(uuid.uuid4()) + file.name

            Project.objects.create(
                name           = data.get('name'),
                user_id        = request.user.id,
                aim_amount     = data.get('aim_amount'),
                description    = data.get('description'),
                end_date       = data.get('end_date')[6:10]+'-'+data.get('end_date')[:2]+'-'+data.get('end_date')[3:5],
                category_id    = data.get('category_id'),
                main_image_url = 'https://humble.s3.ap-northeast-2.amazonaws.com/' + unique_id
            )

            return JsonResponse({'MESSAGE':'SUCCESS'},status = 201)
    
        except KeyError:
            return JsonResponse({'MESSAGE':'ERROR_INPUT_VALUE'}, status=404) 