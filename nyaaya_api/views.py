# coding: utf-8
from django.shortcuts import render

from .models import *
from pyramid.models import *
from configurator.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from configurator.models import *
from seo.views import SeoManager
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from configurator.serializers import *
from configurator.views import *
from traffic_fine.views import *
from law.models import *
from rest_framework import generics
from seo.views import SeoManager
from django.db.models import CharField, Count, Value as V

from law.serializers import *
from law.catalogue import *
from pyramid.serializers import *


class HomePage(APIView):
   def get(self, request, format=None):
        explainers = []
        tocs = AppTOCHomeExplainerMap.objects.all()
        for temap in tocs:
            exp = {}
            exp['title'] = temap.toc.pyramid_doc.title
            exp['url'] = temap.toc.get_absolute_url()
            if temap.toc.get_illustration_url() is not None:
                exp['image_desktop'] =  temap.toc.get_illustration_url()
            #exp['image_mobile'] = temap.image.mobile.url
            else:
                exp['image_desktop'] = ''
            #exp['image_mobile'] = ''
            explainers.append(exp)

        serializer = AppTocExplainerMapSerializer(explainers, many=True)
        url ="/homepage/"
        seomanager=SeoManager(url)
        seomanager.title= "Nyaaya - India's Laws Explained"
        seomanager.description="India's first free online repository of every central and state law. Explained in simple English."
        seomanager.canonical = url
        seo=seomanager.getSerializer()
        shared_data = {
        'home_explainers_items':serializer.data,
        'seo' : seo.data,
        }
        return Response(shared_data)

class TrafficFineListPage(APIView):
    def get(self, request,slug=None):
        trafficFineCategory = TrafficFineCategory.objects.all().order_by('order')
        trafficFineCity = TrafficFineCity.objects.all().order_by('order')
        trafficFines = TrafficFineViewSet.as_view({'get': 'list'})(request).render().content
        url = "/traffic-fine/"
        city = self.request.query_params.get('city', '7')
        category = self.request.query_params.get('category', None)
        title = "Know your traffic fine | Traffic Fine App by Nyaaya"
        description = "Indian Traffic Fines Cheatsheet"
        if city != '7' or category is not None:
            title =''
            description = ''
        if city != '7':
            try:
                cityObj = TrafficFineCity.objects.get(id=city)
                title = cityObj.name + " traffic fine "
                description = cityObj.name + "'s traffic fine list "
                url = "/traffic-fine/" + slugify(cityObj.name) + "/"
            except TrafficFineCity.DoesNotExist:
                pass
        if category is not None:
            try:
                categoryObj = TrafficFineCategory.objects.get(id=category)
                title = title + categoryObj.name + " rules and regulations "
                description = description + categoryObj.name + " "
                url = "/traffic-fine/" + slugify(categoryObj.name)+"/"
            except TrafficFineCategory.DoesNotExist:
                pass
        if city != '7' or category is not None:
            title = title + "| Traffic Fine App by Nyaaya"
            description = description + " - Indian Traffic Fines Cheatsheet"
        if city != '7' and category is not None:
            url = "/traffic-fine/" + slugify(cityObj.name) +"-"+ slugify(categoryObj.name)+"/"
        seomanager =SeoManager(url)
        seomanager.title=title
        seomanager.description=description
        seomanager.canonical = url
        seomanager.og_type='website'
        seo = seomanager.getSerializer()
        return Response({'trafficFines': json.loads(trafficFines), 'trafficFineCategories': TrafficFineCategorySerializer(trafficFineCategory, many=True).data, 'trafficFineCities': TrafficFineCitySerializer(trafficFineCity, many=True).data, 'seo':seo.data })


class CatalogueByCategories(APIView):

    def get(self,request):
        categories=get_all_categories_with_count()
        serializer =CatalogueWebDocSerializer(categories, many=True)
        url="/catalogue/category/"
        seomanager=SeoManager(url)
        seomanager.title="Browse Indian Laws on Nyaaya.in"
        seomanager.description="India's Laws Explained | Browse Indian Laws on Nyaaya.in"
        seomanager.canonical=url
        seo=seomanager.getSerializer()

        return Response({'catalogueitems':serializer.data,
        'seo':seo.data,
        'header': 'tabs',
        'header_text': 'All Laws',
        'list_type': 'catalogue',
        'header_prev_link': '',
        'breadcrumbs': []})


class AppPage(viewsets.ViewSet):
    def getlang(self,request,toc_slug, lang=None):
        return self.list(request,toc_slug,lang)

    def list(self, request, toc_slug, lang=None):
        """
        Return information for a nav in app page.
        """
        langChoice=request.LANGUAGE_CODE
        if langChoice == "hi":
            langChoice = NyaayaApp.HINDI
        else:
            langChoice = NyaayaApp.ENG

        toc_slugs = []
        toc_slugs = toc_slug.split('/')
        num_slugs = len(toc_slugs)

        try:
            appTOC = AppTOC.objects.get(slug=toc_slugs[0],app__lang=langChoice,parent=None)
            nyaayaApp = appTOC.app
        except AppTOC.DoesNotExist:
            raise Http404

        selectedTOC = None
        if num_slugs == 1:
            selectedTOC = appTOC
        else:
            selectedTOCsQuery = AppTOC.objects.filter(app=nyaayaApp,slug=toc_slugs[-1])
            for sq in selectedTOCsQuery:
                if langChoice == NyaayaApp.HINDI:
                    ancestor_slugs = sq.get_absolute_url()[4:-1].split('/')
                else:
                    ancestor_slugs = sq.get_absolute_url()[1:-1].split('/')

                if ancestor_slugs == toc_slugs:
                    selectedTOC = sq
                    break

        if selectedTOC is None:
            raise Http404
        elif selectedTOC.pyramid_doc is None:
            raise Http404

        """
        adds related content data to the API response
        """
        '''
        related_content = ReadMoreContent.objects.filter(
            Q(toc_related__app__theme=NyaayaApp.DEFAULT) | Q(toc_related__app__theme=NyaayaApp.WOLF),
            toc_parent = selectedTOC,
            toc_related__is_deleted=False,
            toc_related__app__is_deleted=False,
            toc_related__pyramid_doc__is_deleted=False,
            toc_related__pyramid_doc__is_draft=False
        ).exclude(toc_related__pyramid_doc=None)[:4]

        read_more_content = []
        for read_more_obj in related_content:

            read_more_content.append({
                'name': read_more_obj.toc_related.pyramid_doc.title,
                'illustration': read_more_obj.toc_related.get_illustration_url(),
                'url': read_more_obj.toc_related.get_absolute_url()
            })

        readMore = ReadMoreContentSerializer(read_more_content, many=True)
        '''

        pyramidDoc = selectedTOC.pyramid_doc
        nyaayaAppSerializer = NyaayaAppSerializer(nyaayaApp)
        pyramidDocSerializer = PyramidDocSerializer(pyramidDoc)
        tocs = appTOC.get_json()


        nxtTOCJSON = None
        prvTOCJSON= None
        nxtTOC = selectedTOC.get_next_toc()
        if nxtTOC:
            nxtTOCJSON = AppTOCSerializer(nxtTOC).data
        prvTOC = selectedTOC.get_prev_toc()
        if prvTOC:
            prvTOCJSON = AppTOCSerializer(prvTOC).data

        urls = {
            'current': selectedTOC.get_absolute_url(),
            'next':    nxtTOCJSON,
            'prev':    prvTOCJSON
        }


        seomanager = SeoManager(selectedTOC.get_absolute_url())
        seomanager.title = pyramidDoc.title
        seomanager.description = strip_tags(pyramidDoc.plain_text)[0:250] + '..'
        seomanager.canonical = selectedTOC.get_absolute_url()
        seomanager.og_type='article'
        seomanager.updated_at = pyramidDoc.updated_at
        seoData = seomanager.getSerializer()
        return Response({'seo':seoData.data,'app': nyaayaAppSerializer.data, 'doc': pyramidDocSerializer.data, 'urls': urls, 'tocs': tocs, 'related_content': []})




def smart_truncate(content, length=100, suffix=' ...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix


def set_description(description):
    if description is None:
        return None
    else:
        return smart_truncate(description, 160)


class CobaltDoc(object):
    pass


class LDPView(viewsets.ViewSet):
    def get(self, request, pk):
        layout = 2

        try:
            webDoc = WebDoc.objects.get(pk=pk, is_deleted=False)
            document_id = webDoc.document_id
            title = webDoc.short_title
        except WebDoc.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

        try:
            webDocXmlData = WebDocXmlData.objects.get(webdoc=webDoc)
            toc_list = json.loads(webDocXmlData.toc_json)['toc']
            nav_toc = []
            for toc in toc_list:
                if toc.get('id', None) is not None:

                    t = {
                        'title': smart_truncate(toc['title'].replace(u'.—', ''),75),
                        'hash' : toc['id']
                        }
                    children = toc.get('children', None )

                    if children is not None and len(children):
                        t['children'] = []
                        for c in children:
                            tc = {
                                'title' : smart_truncate(c['title'].replace(u'.—', ''),75),
                                'hash' : c['id']
                            }
                            t['children'].append(tc)

                    nav_toc.append(t)

                elif toc.get('type',None) is not None and toc.get('type',None) == 'doc':
                    t = {
                        'title' : smart_truncate(toc['title'].replace(u'.—', ''),75),
                        'hash'  : 'component-'+toc['title'].replace(" ","").lower()
                    }
                    nav_toc.append(t)
        except WebDocXmlData.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

        try:
            intro  = DocExplainerBlock.objects.get(webdoc=webDoc,section_id='intro')
            intro_text = intro.text
        except DocExplainerBlock.DoesNotExist:
            intro_text = None

        url = reverse('ldp', kwargs={'pk': pk})
        seoData = SeoManager(url)

        if intro_text:
            seoData.title = '[ Explained ] ' + webDoc.short_title + ' | Nyaaya.in '
            seoData.description = set_description(strip_tags(" ".join(intro.text.split())))
        else:
            seoData.title =  webDoc.short_title + ' | Nyaaya.in '

        seoData.canonical = webDoc.get_url()

        seo = seoData.getSerializer()

        # Getting HTML
        cobaltDoc = CobaltDoc()

        cobaltDoc.id = webDoc.document_id
        cobaltDoc.frbr_uri = webDoc.frbr_url
        cobaltDoc.title = webDoc.short_title
        cobaltDoc.country = 'in'
        cobaltDoc.language = 'en'
        cobaltDoc.draft = False
        cobaltDoc.expression_date = webDoc.date
        cobaltDoc.document_xml = webDocXmlData.xml_data

        root = etree.fromstring(cobaltDoc.document_xml)

        nsmap = {}
        # Hack as etree does not allow empty namespace
        nsmap['ny'] = root.nsmap[None]

        html_cleanup = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" [
                    <!ENTITY nbsp ' '>
                    <!ENTITY lsquo "'">
                    <!ENTITY rsquo "'">
                    <!ENTITY ndash "-">
                    <!ENTITY mdash "-">
                    <!ENTITY ldquo '"'>
                    <!ENTITY rdquo '"'>
                    <!ENTITY shy '-'>
                    <!ENTITY hellip "...">


                    ]>'''

        try:
            explainers  = DocExplainerBlock.objects.filter(webdoc=webDoc).exclude(section_id='intro').order_by('id')
            for explain in explainers:
                layout = 3
                e = root.find('.//ny:section[@id="'+explain.section_id+'"]', nsmap)
                if e is not None:
                    explain.text = explain.text.replace('<p></p>', '<enewline></enewline>')
                    explain.text = explain.text.replace('<br/>', '<enewbr></enewbr>')

                    xml_text = '<explain><div id="explainer-'+ str(explain.id) +'">'+explain.text.replace('\r\n', '')+'</div></explain>'

                    x = etree.fromstring(html_cleanup + xml_text)
                    e.append(x)

                e = root.find('.//ny:chapter[@id="'+explain.section_id+'"]', nsmap)
                if e is not None:
                    explain.text = explain.text.replace('<p></p>', '<enewline></enewline>')
                    explain.text = explain.text.replace('<br/>', '<enewbr></enewbr>')

                    xml_text = '<explain><div id="explainer-'+ str(explain.id) +'">'+explain.text.replace('\r\n', '')+'</div></explain>'

                    x = etree.fromstring(html_cleanup + xml_text)
                    e.set('explained-chapter','1')
                    e.append(x)

        except DocExplainerBlock.DoesNotExist:
            pass

        if request.user.is_authenticated and request.user.is_staff:

            for section in  root.findall(".//ny:section", nsmap):
                num = section.find('./ny:num',nsmap)
                num.set('explainurl','/law/explain/'+str(document_id)+'/section-'+num.text.split(".")[0])

            for chapter in  root.findall(".//ny:chapter", nsmap):
                num = chapter.find('./ny:num',nsmap)
                num.set('explainurl','/law/explain/'+str(document_id)+'/chapter-'+num.text.split(".")[0])
        else:
            for section in  root.findall(".//ny:section", nsmap):
                num = section.find('./ny:num',nsmap)
                num.set('explainurl','#section-'+num.text.split(".")[0])

            for chapter in  root.findall(".//ny:chapter", nsmap):
                num = chapter.find('./ny:num',nsmap)
                num.set('explainurl', '#chapter-'+num.text.split(".")[0])

        if layout == 3:

            xsl_path = os.path.abspath(os.path.join(os.path.dirname(__file__)+'/explained_act.xsl'))
        else:
            xsl_path = os.path.abspath(os.path.join(os.path.dirname(__file__)+'/plain_act.xsl'))

        cobaltDoc.document_xml = etree.tostring(root)

        cobalt_kwargs = {}
        cdoc = CobaltHTMLRenderer(act=cobaltDoc, xslt_filename=xsl_path, **cobalt_kwargs)
        cdoc_html = cdoc.render_xml(cobaltDoc.document_xml)

        return Response({
            'title': title,
            'id': webDoc.document_id,
            'is_stub': webDoc.is_stub,
            'updated_at': webDoc.updated_at,
            'intro': intro_text,
            'html': cdoc_html,
            'nav_toc': nav_toc,
            'layout': layout,
            'seo': seo.data
        }, status=status.HTTP_200_OK)


class CatalogueForCategory(APIView):
    def get(self,request,category_id,category_slug):

        localities=get_all_jurisdiction_with_count(category_id)
        serializer =CatalogueWebDocSerializer(localities, many=True)
        url="/catalogue/category/"+slugify(category_id)+"/"+slugify(category_slug)+"/"
        seomanager=SeoManager(url)
        seomanager.title=get_category_name(category_id)
        seomanager.description=seomanager.title + " | Browse Indian Laws on Nyaaya.in"
        seomanager.canonical=url
        seo=seomanager.getSerializer()

        return Response({'catalogueitems':serializer.data,
        	'header': 'text',
        	'seo':seo.data,
        'header_text': get_category_name(category_id),
        	'header_prev_link': reverse('catalogue-category'),
        	'list_type': 'catalogue',
        'breadcrumbs': [
            {'title':'All Laws','url':reverse('catalogue-by-category')},
            {'title':get_category_name(category_id),'url':None},
        ],
        })

class CatalogueByJurisdiction(APIView):
    def get(self,request):
        localities=get_all_jurisdiction_with_count()
        serializer =CatalogueWebDocSerializer(localities, many=True)
        url="/catalogue/jurisdiction/"
        seomanager=SeoManager(url)
        seomanager.title="Browse Indian Laws on Nyaaya.in"
        seomanager.description="India's Laws Explained | Browse Indian Laws on Nyaaya.in"
        seomanager.canonical=url
        seo=seomanager.getSerializer()
        return Response({'catalogueitems':serializer.data,'seo':seo.data,'header': 'tabs',
        'header_text': 'All Laws',
        'list_type': 'catalogue',
        'header_prev_link': '',
        'breadcrumbs': []})



class CatalogueForCateoryForJurisdiction(APIView):
    def get(self,request,category,category_slug,locality,jurisdiction_slug):
        webDocs = get_webDocs_for_category_jurisdiction(category,locality)
        if webDocs is not None and len(webDocs):
            docs = get_webdoc_items(webDocs)

        serializer =CatalogueWebDocJurisdictionSerializer(docs, many=True)
        url="/catalogue/category/"+slugify(category)+"/"+slugify(category_slug)+"/jurisdiction/"+slugify(locality)+"/"+slugify(jurisdiction_slug)+"/"
        seomanager=SeoManager(url)
        seomanager.title=get_jurisdiction_name(locality) + ' Laws -  ' + get_category_name(category)
        seomanager.description=seomanager.title + " | Browse Indian Laws on Nyaaya.in"
        seomanager.canonical=url
        seo=seomanager.getSerializer()

        return Response({'catalogueitems':serializer.data,
        'seo':seo.data,
        'header_text': get_jurisdiction_name(locality) + ' Laws -  ' + get_category_name(category),
        'header': 'text',
        'list_type': 'webdoc',
        'header_prev_link': reverse('catalogue-category', args=[category, category_slug]),
        'breadcrumbs': [
            {'title':'All Laws','url':reverse('catalogue-by-category')},
            {'title':get_category_name(category),'url':reverse('catalogue-for-category', args=[category, category_slug])},
            {'title':get_jurisdiction_name(locality),'url':None},

        ]})

class CatalogueForJurisdiction(APIView):
    def get(self,request,locality,jurisdiction_slug):
        catalogueitems = get_all_categories_with_count(locality)
        serializer =CatalogueWebDocSerializer(catalogueitems, many=True)
        url="/catalogue/jurisdiction/"+slugify(locality)+"/"+slugify(jurisdiction_slug)+"/"
        seomanager=SeoManager(url)
        seomanager.title= get_jurisdiction_name(locality)
        seomanager.description=seomanager.title + " | Browse Indian Laws on Nyaaya.in"
        seomanager.canonical=url
        seo=seomanager.getSerializer()
        return Response({'catalogueitems':serializer.data,'seo':seo.data,'header': 'text',
        'header_text': get_jurisdiction_name(locality) + ' Laws',
        'list_type': 'catalogue',
        'header_prev_link': reverse('catalogue-jurisdiction'),
        'breadcrumbs': [
            {'title':'All Laws','url':reverse('catalogue-by-category')},
            {'title':get_jurisdiction_name(locality),'url':None},
        ]
    })

class GuidesPage(APIView):
    def get(self,request):

        url="/guides/"
        seoData =SeoManager(url)
        seoData.title = "Nyaaya - India's Laws Explained"
        seoData.description= "India's first free online repository of every central and state law. Explained in simple English."
        seoData.canonical=url
        seo = seoData.getSerializer()
        return Response({'seo':seo.data})

class LawExplainersPage(APIView):
    def get(self,request):
        explainers = []
        langCode=request.LANGUAGE_CODE
        langChoice=request.LANGUAGE_CODE
        if langChoice == "hi":
            langChoice = NyaayaApp.HINDI
        else:
            langChoice = NyaayaApp.ENG

        tocs = AppTOCExplainerMap.objects.filter(toc__app__lang=langChoice)
        for temap in tocs:

            exp = {}
            exp['title'] = temap.toc.pyramid_doc.title
            exp['url'] = temap.toc.get_absolute_url()
            exp['short_title'] = ''

            if temap.toc.get_illustration_url() is not None:
                exp['image_desktop'] =  temap.toc.get_illustration_url()
            else:
                exp['image_desktop'] = ''
            explainers.append(exp)

        explainers=ExplainerSerializer(explainers, many=True)
        url=langCode+"/law-explainers/"
        seomanager = SeoManager(url)
        seomanager.canonical=url
        seoData =seomanager.getSerializer()
        shared_data={
        'explainers':explainers.data,
        'seo':seoData.data,
        }

        return Response(shared_data)




class CatalogueForJurisdictionForCateory(APIView):
    def get(self,request,locality,jurisdiction_slug,category,category_slug):
        webDocs = get_webDocs_for_category_jurisdiction(category,locality)

        if webDocs is not None and len(webDocs):
            docs = get_webdoc_items(webDocs)
        serializer =CatalogueWebDocJurisdictionSerializer(docs, many=True)
        url = "catalogue/jurisdiction/"+slugify(locality)+"/"+slugify(jurisdiction_slug)+"/category/"+slugify(category)+"/"+slugify(category_slug)+"/"
        seomanager=SeoManager(url)
        seomanager.title=get_jurisdiction_name(locality)  + ' Laws - ' + webDocs[0].category
        seomanager.description=seomanager.title + " | Browse Indian Laws on Nyaaya.in"
        seomanager.canonical = url
        seo=seomanager.getSerializer()

        shared_data = {
            'catalogueitems':serializer.data,
            'seo': seo.data,
            'header_text':get_jurisdiction_name(locality)  + ' Laws - ' + webDocs[0].category,
            'header': 'text',
            'list_type': 'webdoc',
            'header_prev_link': reverse('catalogue-jurisdiction', args=[locality, jurisdiction_slug]),
            'breadcrumbs': [
                {'title':'All Laws','url':reverse('catalogue-by-category')},
                {'title':get_jurisdiction_name(locality),'url':reverse('catalogue-for-jurisdiction', args=[locality, jurisdiction_slug])},
                {'title':webDocs[0].category,'url':None},

            ]
        }
        return Response(shared_data)

class GuideIntro(APIView):

    def get(self,request,doc_id,slug=None):
        webDoc = WebDoc.objects.get(pk=doc_id)
        docIntro = webDoc.explainer.get(section_id='intro')
        guide ={}
        guide['data']  = docIntro.text
        guide['short_title'] = webDoc.short_title
        guide['url'] = webDoc.get_absolute_url()
        serializer = GuideIntroSerializer(guide)
        #@TODO: use reverse
        url = "/law-explainers/"+slugify(doc_id)+"/"+slugify(slug)+"/"
        seomanager =SeoManager(url)
        seomanager.title = "Nyaaya - India's Laws Explained"
        seomanager.description = "India's first free online repository of every central and state law. Explained in simple English."
        seomanager.canonical =  url
        seoData =seomanager.getSerializer()
        shared_data = {
            'guide_intro' : serializer.data,
            'seo' : seoData.data
        }
        return Response(shared_data)


class WriteToUs(APIView):
    def get(self,request):
        url="/write-to-us/"
        seomanager =SeoManager(url)
        seomanager.title = "Write to us | Nyaaya.in"
        seomanager.canonical = url
        seoData =seomanager.getSerializer()
        return Response({'seo':seoData.data})
