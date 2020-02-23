from rest_framework_nested import routers

from . import viewsets

router = routers.DefaultRouter()
router.register('members', viewsets.MemberViewset)

member_router = routers.NestedSimpleRouter(
    parent_router=router,
    parent_prefix='members',
    lookup='member'
)
member_router.register(
    prefix='fields',
    viewset=viewsets.MemberFieldViewset,
    basename='member-fields'
)

urlpatterns = router.urls
urlpatterns += member_router.urls
