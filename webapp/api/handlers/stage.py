from django.views import View
from django.conf import settings
from django.core import serializers
from django.forms import model_to_dict

from api.helpers.mixins import AuthRequiredMixin
from api.helpers.http.jsend import JSENDSuccess, JSENDError
from api.models.resources import Membership, Stage

import json
import jwt


RES_FIELDS = ['id', 'title', 'endpoint', 'status', 'repo', 'branch', 'commits', 'created_at']


class StageRootHandler(AuthRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        org = Membership.get_org_of_user(request.user)
        if not org:
            return JSENDError(status_code=400, msg='org not found')

        stages_qs = Stage.objects.filter(org=org)
        stages = [model_to_dict(s, fields=RES_FIELDS) for s in stages_qs]
        return JSENDSuccess(status_code=200, data=stages)

    def post(self, request, *args, **kwargs):
        json_body = json.loads(request.body)
        title = json_body.get('title')
        repo = json_body.get('repo')
        branch = json_body.get('branch')

        if not (title and repo and branch):
            return JSENDError(status_code=400, msg='invalid stage info')

        org = Membership.get_org_of_user(request.user)
        if not org:
            return JSENDError(status_code=400, msg='org not found')

        stage = Stage.objects.create(org=org, title=title, repo=repo, branch=branch)
        stage_dict = model_to_dict(stage, fields=RES_FIELDS)
        return JSENDSuccess(status_code=200, data=stage_dict)


class StageDetailHandler(AuthRequiredMixin, View):
    def get(self, request, stage_id, *args, **kwargs):
        org = Membership.get_org_of_user(request.user)
        if not org:
            return JSENDError(status_code=400, msg='org not found')

        try:
            stage = Stage.objects.get(org=org, id=stage_id)
        except Stage.DoesNotExist:
            return JSENDError(status_code=404, msg='stage not found')

        stage_dict = model_to_dict(stage, fields=RES_FIELDS)
        return JSENDSuccess(status_code=200, data=stage_dict)

    def put(self, request, stage_id, *args, **kwargs):
        json_body = json.loads(request.body)
        title = json_body.get('title')
        repo = json_body.get('repo')
        branch = json_body.get('branch')
        status = json_body.get('status')
        commits = json_body.get('commits')
        endpoint = json_body.get('endpoint')

        org = Membership.get_org_of_user(request.user)
        if not org:
            return JSENDError(status_code=400, msg='org not found')

        try:
            stage = Stage.objects.get(org=org, id=stage_id)
        except Stage.DoesNotExist:
            return JSENDError(status_code=404, msg='stage not found')

        stage.title = title if title else stage.title
        stage.repo = repo if repo else stage.repo
        stage.branch = branch if branch else stage.branch
        stage.status = status if status else stage.status
        stage.commits = commits if commits else stage.commits
        stage.endpoint = endpoint if endpoint else stage.endpoint
        stage.save()

        stage_dict = model_to_dict(stage, fields=RES_FIELDS)
        return JSENDSuccess(status_code=204, data=stage_dict)


    def delete(self, request, stage_id, *args, **kwargs):
        org = Membership.get_org_of_user(request.user)
        if not org:
            return JSENDError(status_code=400, msg='org not found')

        try:
            stage = Stage.objects.get(org=org, id=stage_id)
        except Stage.DoesNotExist:
            return JSENDError(status_code=404, msg='stage not found')

        stage.delete()
        return JSENDSuccess(status_code=204, data={})