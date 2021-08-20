import json

from datetime import datetime

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Q, Sum, Count

from projects.models        import Project, Patron, Option, Category, Tag

from utils import log_in_confirm

class ProjectListView(View):
    def get(self, request):

        category_id = request.GET.get("categoryId")
        
        q = Q()

        if category_id:
            q &= Q(category_id = category_id)
        
        limit        = int(request.GET.get('limit', 12))
        offset       = int(request.GET.get('offset', 0))

        projects = [{
                "id"             : project.id,
                "category_id"    : project.category_id,
                "user_id"        : project.user_id,
                "user_name"      : project.user.nickname,
                "name"           : project.name,
                "image"          : project.main_image_url,
                "aim_amount"     : project.aim_amount,
                "created_at"     : project.created_at,
                "end_date"       : project.end_date, 
                "description"    : project.description
            } for project in Project.objects.filter(q).order_by('created_at')[offset:offset+limit]]
            
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
                    "id"          : project.id,
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

    @log_in_confirm
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
