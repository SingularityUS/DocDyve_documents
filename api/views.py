from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from .search_indexes import DocumentIndex
from haystack.query import SearchQuerySet
from .qa import answer_question

class DocumentUploadView(generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = DocumentSerializer

class DocumentListView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

class DocumentSearchView(generics.ListAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = DocumentSerializer

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES['file']
        document = Document.objects.create(file=file_obj)

        # Reindex the document for searching
        DocumentIndex().update_object(document)

        # Perform a semantic search on the uploaded documents
        question = request.POST.get('question', '')
        results = SearchQuerySet().filter(text=question).models(Document).load_all()

        # Get the best answer using the QA script
        if results:
            best_answer = answer_question(question, [result.object.file.path for result in results])
            return Response({'answer': best_answer})
        else:
            return Response({'answer': 'No results found.'}, status=status.HTTP_404_NOT_FOUND)