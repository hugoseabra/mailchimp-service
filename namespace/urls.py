from rest_framework_nested import routers

from . import viewsets

router = routers.DefaultRouter()
router.register('namespaces', viewsets.NamespaceViewset)

namespace_router = routers.NestedSimpleRouter(
    parent_router=router,
    parent_prefix='namespaces',
    lookup='namespace'
)
namespace_router.register(
    prefix='lists',
    viewset=viewsets.MailChimpListViewset,
    basename='namespace-lists'
)
namespace_router.register(
    prefix='fields',
    viewset=viewsets.ListFieldViewset,
    basename='namespace-fields'
)

urlpatterns = router.urls
urlpatterns += namespace_router.urls
