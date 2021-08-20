import json

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Q
from django.core.exceptions import FieldError

from projects.models        import Project

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
