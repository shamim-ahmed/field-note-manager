from django.http import HttpResponse, HttpResponseForbidden
from django.template import Context, loader
from fieldNoteManager.models import User, Excursion, Sighting
from httplib import HTTPConnection
import urllib
from lxml import etree

# returns the home page
def index(request):
    c = Context()
    
    if 'user' in request.session:
        c.__setitem__('user', request.session['user'])
        excursions = Excursion.objects.filter(user=request.session['user'])
        c.__setitem__('excursions', excursions)
        
    return homepage(request, c)


# checks if the submitted credentials are valid
# this method also adds a 'user' object to the session
def login(request):
    uname = ''
    pwd = ''
    
    if 'userName' in request.POST and request.POST['userName'] and 'password' in request.POST and request.POST['password']:
        uname = request.POST['userName']
        pwd = request.POST['password']
            
    c = Context()
    users = User.objects.filter(userName=uname,password=pwd) 
    
    if len(users) > 0:
        user = users[0]
        request.session['user'] = user
        c.__setitem__('user', user)
        excursions = Excursion.objects.filter(user=user)
        c.__setitem__('excursions', excursions)
    
    if 'user' not in c:
        c.__setitem__('errorMessage', 'Authentication Failure')
        
    return homepage(request, c)


# logs out the user by removing the 'user' object from the session
def logout(request):
    if 'user' in request.session:
        del request.session['user']
        
    return index(request)


# shows the registration form
def showRegisterForm(request):  
    c = Context()
    t = loader.get_template("templates/registerForm.html")  
    return HttpResponse(t.render(c))


# registers the user
def register(request):
    t = None
    c = Context()
    
    if 'userName' in request.POST and request.POST['userName'] and 'password' in request.POST and request.POST['password']:
        name = request.POST['userName']
        passwd = request.POST['password']
        users = User.objects.filter(userName=name)
        
        if len(users) > 0:
            c.__setitem__('errorMessage', 'A user with the userName %s already exists' % name)
            t = loader.get_template("templates/registerForm.html")
        else:
            user = User()
            user.userName = name
            user.password = passwd
            user.save()
            t = loader.get_template('templates/registerSuccess.html')
    else:
        c.__setitem__('errorMessage', 'Both userName and password must be specified')
        t = loader.get_template("templates/registerForm.html")
    
    return HttpResponse(t.render(c))


# shows the form that allows a logged-in user to add excursion location, date and time
def showLocationForm(request):
    if 'user' not in request.session:
        return HttpResponseForbidden(loader.get_template("templates/403.html").render(Context()))
    
    t = loader.get_template('templates/locationForm.html')
    c = Context()
    c.__setitem__('user', request.session['user'])
    return HttpResponse(t.render(c))      


# adds an excursion to database after the location, date and time has been submitted
def addLocation(request):
    if 'user' not in request.session:
        return HttpResponseForbidden(loader.get_template("templates/403.html").render(Context()))
    
    c = Context()

    if 'location' in request.POST and request.POST['location'] and 'date' in request.POST and request.POST['date'] and 'time' in request.POST and request.POST['time']:
        excursion = Excursion()
        excursion.user = request.session['user']
        excursion.location = request.POST['location']
        excursion.date = request.POST['date']
        excursion.time = request.POST['time']
        excursion.save()
        c.__setitem__('user', request.session['user'])
        c.__setitem__('excursion', excursion)
        t = loader.get_template('templates/sightingForm.html')
        
    return HttpResponse(t.render(c))


# adds a specific observation/sighting to the database
# this method is called via AJAX
def addSighting(request):
    if 'user' not in request.session:
        return HttpResponseForbidden(loader.get_template("templates/403.html").render(Context()))
    
    result = 'failure'
    
    if 'excursionId' in request.POST and request.POST['excursionId'] and 'species' in request.POST and request.POST['species']:
        excursions = Excursion.objects.filter(id=request.POST['excursionId'])
        
        if len(excursions) > 0:
            sighting = Sighting()
            sighting.excursion = excursions[0]
            sighting.species = request.POST['species']
            sighting.save()
            result = 'success'
            
    return HttpResponse(result) 


# performs a search by location name
def searchByLocation(request):
    c = Context()
    sightingList = []
    
    if 'location' in request.GET and request.GET['location']:
        c.__setitem__('location', request.GET['location'])
        excursions = Excursion.objects.filter(location=request.GET['location'])
        
        if excursions:
            for excur in excursions:
                sightings = Sighting.objects.filter(excursion=excur)
                
                for s in sightings:
                    sightingList.append(s)

    c.__setitem__('sightings', sightingList)
    t = loader.get_template("templates/locationSearchResult.html")
    return HttpResponse(t.render(c))
    

# performs a search by species name
def searchBySpecies(request):
    c = Context()
    sightingList = []
    
    if 'species' in request.GET and request.GET['species']:
        c.__setitem__('species', request.GET['species'])
        sightingList = Sighting.objects.filter(species=request.GET['species'])
        
    c.__setitem__('sightings', sightingList)
    t = loader.get_template('templates/speciesSearchResult.html')
    return HttpResponse(t.render(c))
    

# performs a wild card search for either location or species name
# this method is called during the generation of suggestions while the user is typing
def wildCardSearch(request):
    result = []
    
    if 'location' in request.GET and request.GET['location']:
        loc = request.GET['location']
        excursions = Excursion.objects.filter(location__startswith=loc)
                
        for excur in excursions:
            if  excur.location not in result:
                result.append(excur.location)
                                       
    elif 'species' in request.GET and request.GET['species']:
        spec = request.GET['species'] 
        sightings = Sighting.objects.filter(species__startswith=spec)
        
        for sighting in sightings:
            if sighting.species not in result:
                result.append(sighting.species)
            
            
    return HttpResponse(", ".join(result))


# renders the Google map for a particular location
def showMap(request):
    c = Context()
    
    if 'location' in request.GET and request.GET['location']:
        loc = request.GET['location']
        c.__setitem__('locationName', loc)
        params = urllib.urlencode({"q": loc})
        conn = HTTPConnection("where.yahooapis.com")
        conn.request("GET", "/geocode?%s" % params)
        resp = conn.getresponse()
        
        if resp.status == 200:
            data = resp.read()
            root = etree.XML(data)
            resultNodes = root.xpath('/ResultSet/Result')
            locationList = []
            idx = 0
                        
            for node in resultNodes:
                idx += 1
                locinfo = LocationInfo()
                locinfo.location = loc
                locinfo.latitude = float(node.xpath('latitude')[0].text)
                locinfo.longitude = float(node.xpath('longitude')[0].text)
                locinfo.city = node.xpath('city')[0].text
                locinfo.state = node.xpath('state')[0].text
                locinfo.country = node.xpath('country')[0].text
                locinfo.divId = 'map_canvas_%d' % idx 
                locationList.append(locinfo)
                
            c.__setitem__('locationList', locationList) 
        
    t = loader.get_template("templates/googleMap.html")
    return HttpResponse(t.render(c))


# renders search result from Wikipedia for a particular species name
def showWikipediaLinks(request):
    c = Context()
    
    if 'species' in request.GET and request.GET['species']:
        species = request.GET['species']
        c.__setitem__('species', species)
        params = urllib.urlencode({"action":"opensearch", "search":species, "format":"xml"})
        conn = HTTPConnection("en.wikipedia.org")
        headerMap = {"User-Agent" : "Shamim Ahmed (shamim.buet.99@gmail.com)"}
        conn.request("GET", "/w/api.php?%s" % params, headers=headerMap)
        resp = conn.getresponse()
        
        if resp.status == 200:
            data = resp.read()
            root = etree.XML(data)
            namespaceMap = {'n':'http://opensearch.org/searchsuggest2'}
            itemNodes = root.xpath("/n:SearchSuggestion/n:Section/n:Item", namespaces=namespaceMap)
            wikiEntryList = []
            
            for item in itemNodes:
                wikiEntry = WikiEntryInfo()
                imageNodes = item.xpath("n:Image", namespaces=namespaceMap)
                textNode = item.xpath("n:Text", namespaces=namespaceMap)[0]
                descriptionNode = item.xpath("n:Description", namespaces=namespaceMap)[0]
                urlNode = item.xpath("n:Url", namespaces=namespaceMap)[0]
                
                wikiEntry.title = textNode.text
                wikiEntry.description = descriptionNode.text
                wikiEntry.articleUrl = urlNode.text
                
                if len(imageNodes) > 0:
                    wikiEntry.imageUrl = imageNodes[0].get('source')
                    wikiEntry.imageWidth = 2 * int(imageNodes[0].get('width'))
                    wikiEntry.imageHeight = 2 * int(imageNodes[0].get('height'))
                    
                wikiEntryList.append(wikiEntry)
                
            c.__setitem__('wikiEntryList', wikiEntryList)
                    
    t = loader.get_template("templates/wikipedia.html");
    return HttpResponse(t.render(c))


# the following functions are utility functions (they are not directly mapped to any URL)
def homepage(request, c): 
    t = loader.get_template('templates/index.html')
    return HttpResponse(t.render(c))    
            
            

#utility class to contain location related information
class LocationInfo:
    location = str;
    latitude = float;
    longitude = float;
    city = str;
    state = str;
    country = str;
    divId = str;
   
    def __str__(self):
        return self.location 
   
#utility class for wikipedia entry related info
class WikiEntryInfo:
    title = str;
    description = str;
    articleUrl = str;
    imageUrl = str;
    imageWidth = int;
    imageHeight = int;
    
    def __str__(self):
        return self.title