import logging

logger = logging.getLogger()

class ProjectView():
    @login_decorator
    def post(self, request):
        try:
            user = request.user
            data = request.POST
            cloud_storage = CloudStorage(ACCESS_KEY_ID, SECRET_ACCESS_KEY, bucket)

            image = request.FILES.get('image')
            input_date = data.get('end_date')

            if not image:
                return JsonResponse({'MESSAGE' : 'IMAGE_EMPTY'}, status=400)


           Project.objects.create(
                name           = data.get('name'),
                user_id        = user.id,
                aim_amount     = data.get('aim_amount'),
                description    = data.get('description'),
                end_date       = input_date[6:10]+'-'+input_date[:2]+'-'+input_date[3:5],
                category_id    = data.get('category_id'),
                main_image_url = 'https://humblebug.s3.us-east-2.amazonaws.com/' + upload_key
            )

           cloud_storage.upload_file(file)

            return JsonResponse({'MESSAGE':'SUCCESS'},status = 201)
    
        except KeyError:
            return JsonResponse({'MESSAGE':'ERROR_INPUT_VALUE'}, status=404) 

class CloudSotrage:
    def __init__(self, ACCESS_KEY_ID, SECRET_ACCESS_KEY, bucket):
        self.ACCESS_KEY_ID = ACCESS_KEY_ID
        self.SECRET_ACCESS_KEY = SECRET_ACCESS_KEY
        self.bucket = bucket
        self.client = boto3.client(
            's3',
            aws_access_key_id     = ACCESS_KEY_ID,
            aws_secret_access_key = SECRET_ACCESS_KEY
        )

    def upload_file(self, file):
        unique_id = str(uuid.uuid4()) + file.name
        try:
            return self.client.upload_fileobj(
                file,
                self.bucket,
                unique_id,
                ExtraArgs = {
                    'ContentType' : image.content_type
                }
            )

        except Exception as e:
            logger.error(f" func.name = {..} | error_message = {e}")
