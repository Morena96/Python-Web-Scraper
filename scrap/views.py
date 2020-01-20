from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from lxml import html, etree
import requests
# Create your views here.
@login_required
def A(request):
    user=request.user
    return render(request,"index.html",{'user':user})

@login_required
def scrap(request):
    if request.POST:
        webpageLink = request.POST['url']
        page = requests.get(webpageLink)
        extractedHtml = html.fromstring(page.content)
        imageSrc = extractedHtml.xpath("//img/@src")
        imageDomain = webpageLink.rsplit('/', 1)

        for i in imageSrc:
            if i.startswith("http"):
                imageLink = i
            else:
                imageLink = str(imageDomain[0]) + str(i)
            filename = imageLink.split("/")[-1] 
            rawImage = requests.get(imageLink, stream=True)
            with open(filename, 'wb') as fd:
                for chunk in rawImage.iter_content(chunk_size=1024):
                    fd.write(chunk)
    return render(request,"scraper.html",{'url':webpageLink})

@login_required
def youtube(request):
    url = request.POST['tube']
    video = pafy.new(url)
    bestResolutionVideo = video.getbest()
    bestResolutionVideo.download() 
    return render(request,"scraper.html",{'url':url})
