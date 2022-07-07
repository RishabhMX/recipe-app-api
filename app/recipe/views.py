from django.shortcuts import render

"""
Views for the recipe APIs
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework import (viewsets,mixins)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import (Recipe,Tag,Ingredient)
from recipe import serializers
from rest_framework import (
    viewsets,
    mixins,
    status,
)

@extend_schema_view(  #schema description
    list=extend_schema(
        parameters=[

            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of tag IDs to filter',
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingredient IDs to filter',
            ),
        ]
    )
)


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __params_to_ints(self,qs): #list of comma separated strings
        """Convert a list of strings into integers"""
        return [int(str_id) for str_id in qs.split(',')] #convertin strings to id (strings are seperated by commas)

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        tags=self.request.query_params.get('tags') #getting parameters
        ingredients=self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids=self.__params_to_ints(tags)  #convertings tag string to int
            queryset = queryset.filter(tags__id__in=tag_ids) #filtering through database
        if ingredients:
            ingredient_ids=self.__params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(  #filtering and getting result by id
            user=self.request.user
        ).order_by('-id').distinct() #distinct so duplicate values are not returned


    def get_serializer_class(self):  #overriding get_serializer_class
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self,serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image') #action used for http methods, to make ImageSerializer 'POST' only
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object() #getting recipe
        serializer = self.get_serializer(recipe, data=request.data) # getting serializer i.e. "get_serializer_class"

        if serializer.is_valid():
            serializer.save() #saving image
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter('assigned_only', OpenApiTypes.INT, enum=[0, 1]),
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to recipes.',
            ),
        ]
    )
)


class BaseRecipeAttrViewSet(
                mixins.UpdateModelMixin, #help in creating PUT,POST,GET,DELETE method for the endpoints
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet,):
    """BaseViewSet for Recipe Attribute"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]



    def get_queryset(self): #overrding queryset default function
        """Filter queryset to authenticated user."""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))  #converting to boolean value
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(  #removed self.queryset to queryset so filter can be applied on queryset
            user=self.request.user
        ).order_by('-name').distinct()


class TagViewSet(BaseRecipeAttrViewSet): #Listmdemixin to get list of models
    """Manage tags in the database."""                                #Update mixin to implement the updatetags feature
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()



class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()





