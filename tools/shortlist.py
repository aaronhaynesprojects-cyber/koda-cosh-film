"""Version 2 shortlist: scores by the brief's weights, and the data every V2 document is built from.
Criteria (max): low light 25, architecture & furniture 20, KODA opportunity 20, quality 15, composition 10, continuity 10."""
import json
DEDON_PRESS = "DEDON Press Portal (dedon.world/pressportal -> dedon.kontainer.com, public 'PRESS' access); file marked downloadable"
DEDON_ADV = "DEDON Professionals Portal, Advertising Materials (linked from the dedon.de header); file marked downloadable; DEDON's note: 'ads, instructions and more for your own use'"
R_DEDON = "Published for press and retail partners. Not yet cleared for a KODA/Cosh concept film: needs written OK from DEDON (pr@dedon.de), or via Cosh Living as a DEDON stockist."
R_TRIBU = "Public project page on tribu.com; photograph belongs to the project/hotel or photographer. Not cleared. Tribù's licensed downloads need press-lounge registration (press@tribu.com)."
R_POT = "Public project page on potocco.it; photographer-credited. Not cleared. Potocco's high-res downloads need a registered account (dealer/architect/press)."
S = [
 # id, maker, campaign, title, file, w, h, scores(6), use, light, koda, notes, source
 ("D01","DEDON","Secret Lakeside (Spirit of Place)","Lake house under moonlight","dedon/originals/dedon-secret-lakeside-house-night.jpg",6000,4252,(24,18,16,15,9,8),
  "Opening establishing shot: the house sits dark on the lake, then its lights come up and double in the water.","Blue-hour night, moon, warm interior and facade light already in the render","Arkoslight trimless downlights in the deck soffit; Occhio Mito outdoor-rated wall lights on the stone wing (to confirm in KODA range)","Manufacturer CGI render. Lights-off plate tested: works.","id 11165383; "+DEDON_PRESS),
 ("D02","DEDON","Mysterious Desert (Spirit of Place)","Cliff villa at blue hour","dedon/originals/dedon-mood-mysterious-desert-dala-loon-mbrace-sealine-kida.jpg",1640,984,(25,20,18,5,9,9),
  "'The difference is light': the villa switches on. Paired with D07, the same villa at golden hour.","Blue hour, interior and terrace lit, pool lit","Arkoslight recessed linear in the cantilever soffit; A-N-D Column pendants on the lower terrace","Only 1,640 px wide: 1080p at most. Ask DEDON for the master. Manufacturer CGI. Lights-off plate needs a hand-cut glazing mask.","id 9272801; "+DEDON_PRESS),
 ("D03","DEDON","Mu Mystique","Mountain terrace lounge at dusk","dedon/originals/dedon-mood-mu-mystique-dusk.jpg",6000,4248,(21,19,15,15,9,9),
  "Vision: a KODA floor light completing the lounge.","Dusk, fireplace lit, two DEDON lanterns glowing","Occhio Mito largo arc floor light over the sofa; Pablo Uma cordless lanterns could stand in for DEDON's own","DEDON lanterns already light the scene (competing fittings). Manufacturer CGI.","id 14633133; "+DEDON_PRESS),
 ("D04","DEDON","Spiritual Mountain (Spirit of Place)","Riverside dining under a pergola at dusk","dedon/originals/dedon-spiritual-mountain-bellmonde-kida-ombii.jpg",6000,6000,(20,18,19,15,8,9),
  "Vision: pendants arrive over the dining table. The best pendant opportunity in the set.","Dusk, small table lamps on the table","Occhio Mito sospeso 60 (bronze) or Lodes Volum trio hung from the pergola beams, about 75 cm above the table, 2700 K","Square frame: crop to 16:9 keeps table and river. Manufacturer CGI.","id 11165386; "+DEDON_PRESS),
 ("D05","DEDON","Spiritual Mountain (Spirit of Place)","Canyon pavilion and water terrace","dedon/originals/dedon-mood-spiritual-mountain-mbrace-mu-porcini-roii-the others.jpg",4248,6000,(21,19,16,15,6,8),
  "Opportunity: slow vertical move down the pavilion to the water.","Sunset behind canyon, pavilion lights on","A-N-D Pace pendants in the pavilion; Arkoslight step lights along the deck","Portrait: needs a vertical move or a 16:9 crop. DEDON lanterns in frame.","id 9271947; "+DEDON_PRESS),
 ("D06","DEDON","Secret Lakeside (Spirit of Place)","Stone lake house terrace at dusk","dedon/originals/dedon-mood-secret-lakeside-mbrace-mbrace alu-porcini-mbarq-the others.jpg",5000,3535,(17,17,16,14,9,8),
  "Opportunity: a broad, confident closing room.","Dusk sky, interior and wall lights on, fire pit","Pablo Bola felt pendants under the eaves; Occhio wall lights on the stone piers","DEDON lanterns on the deck. Manufacturer CGI.","id 9272092; "+DEDON_PRESS),
 ("D07","DEDON","Mysterious Desert (Spirit of Place)","Cliff villa at golden hour (same villa as D02)","dedon/originals/dedon-mood-mysterious-desert-loon-mbrace-mbrace-alu-nestrest-sealine.jpg",6000,3661,(10,20,17,15,9,8),
  "Before: daylight falls away to dusk before D02 lights up.","Low golden sun, unlit","As D02","Daylight: scored down on atmosphere, but it is the honest 'before' for D02.","id 9272241; "+DEDON_PRESS),
 ("D08","DEDON","Mysterious Desert","Fire-pit terrace above the desert","dedon/originals/dedon-mood-mysterious-desert-dala.jpg",3508,2480,(22,16,12,13,8,8),
  "Atmosphere insert.","Dusk, fire pit","Pablo Uma cordless lanterns around the pit","Little architecture to light. Manufacturer CGI.","id 9031547; "+DEDON_PRESS),
 ("D09","DEDON","Spiritual Mountain (Spirit of Place)","Dining detail with lamp, portrait","dedon/originals/dedon-spiritual-mountain-bellmonde-kida-ombii-detail.jpg",4244,6000,(19,17,15,15,6,8),
  "Close-up partner to D04.","Dusk","As D04","Portrait. Manufacturer CGI.","id 11165389; "+DEDON_PRESS),
 ("D10","DEDON","Endless Ocean","Sea grotto with hanging swings","dedon/originals/dedon-mood-endless-ocean-orbit-swingrest.jpg",3502,2480,(21,14,9,13,8,7),
  "Atmosphere insert only.","Warm low sun into the grotto, lit cabanas","Limited","No architecture to light.","id 9272268; "+DEDON_PRESS),
 ("D11","DEDON","SEAX","Night campfire in a canyon","dedon/originals/dedon-mood-seax-night.jpg",6000,4250,(24,12,7,14,8,6),
  "Mood only.","Night, fire, DEDON lanterns","Little","Lit by fire and DEDON lanterns.","id 9272507; "+DEDON_PRESS),
 ("V01","DEDON","Spirit of Place brand film","DEDON Video Brand (1:59, 1080p 25p)","dedon/advertising/originals/DEDON Video Brand.mp4",1920,1080,(17,15,8,11,9,8),
  "Live-action dusk: silhouettes against sunset 0:14-0:22; cliff houses 1:20 and 1:44.","Mixed; best clips at sunset","None: used as moving atmosphere","Burned-in words on several shots ('we found', 'Spirit of Place'); use only clean frames.","id 15091997; "+DEDON_ADV),
 ("V02","DEDON","Summer Home campaign","Summer Home teaser (0:47, 1080p 24p)","dedon/advertising/originals/DEDON Video Summer Home Teaser High Res.mp4",1920,1080,(8,15,7,11,8,7),
  "Reserve.","Mostly bright midday; opening beach shot is dark","Little","Daylight.","id 20266648; "+DEDON_ADV),
 ("V03","DEDON","Brand films","Craftsmanship (1:15, 4K 30p)","dedon/advertising/originals/DEDON Video Craftsmanship.mp4",3840,2160,(6,12,4,15,8,7),
  "Material close-ups if a texture insert is wanted.","Workshop","None","Not an environment.","id 15092051; "+DEDON_ADV),
 ("P01","Potocco","Project: Izar Houses","Long dining hall opening to dusk","potocco/originals/Izar-Houses__0cdd81c8-bb2e-480b-9b69-027566978ea6.jpg",4200,2800,(16,19,17,14,9,8),
  "Vision interior: pendants over the long table.","Dusk outside, warm cove light inside, small table lamps","Lodes Random cluster or A-N-D Pebble linear over the table","Real photograph. Existing cove lighting stays.","potocco.it/en/realizzazioni/120/"),
 ("P02","Potocco","Project: Hotel Ansitz Steinbock","Vaulted lounge, low light (photo Alex Moling)","potocco/originals/Hotel-Ansitz-Steinbock__Lounge_mod.jpg",3000,2001,(18,16,15,12,8,8),
  "Interior alternative.","Soft window light, dim room","Occhio Luna sospeso cloud or A-N-D Vale chandelier in place of the existing pendant","Real photograph; existing chandelier would be replaced.","potocco.it/en/realizzazioni/124/"),
 ("T01","Tribù","Project: Villa Geba, Montenegro","Sunset terrace dining over Sveti Stefan","tribu/originals/Villa-Geba_Montenegro.jpg",2832,4256,(17,17,12,12,5,8),
  "Reserve.","Sun in frame, golden","Table lamps only","Portrait; sun in frame; hotel photography.","tribu.com/en/inspiration/projects/villa-geba/"),
 ("T02","Tribù","Project: Abadia Retuerta","Calicata terrace at dusk","tribu/originals/CALICATA-Terroir-Bar_Abadia-Retuerta-LeDomaine-2020-13.JPG",2500,1667,(18,15,12,11,8,6),
  "Reserve.","Real dusk; existing lanterns and candles","Wall lights on the brick facade","Hotel name on the wall; 2,500 px.","tribu.com/en/inspiration/projects/abadia-retuerta/"),
 ("T03","Tribù","Project: Villa Geba","Terrace dining at sunset (photo Michel Figuet)","tribu/originals/Michel-Figuet-6439.jpg",2000,1451,(16,16,13,9,8,8),
  "Reserve.","Sunset","Table and floor lamps","2,000 px only.","tribu.com/en/inspiration/projects/villa-geba/"),
 ("T04","Tribù","Collections 2026 film","Collections 2026 (0:38, Vimeo)","",0,0,(10,16,8,0,8,8),
  "Reference only.","Unknown until viewed in full","-","Streaming copy only; Tribù supplies video through its press download area.","vimeo.com/1161713196 on tribu.com home page"),
]
W=(25,20,20,15,10,10)
out=[]
for s in S:
    sc=dict(zip(("low_light","architecture","koda_opportunity","quality","composition","continuity"),s[7])); tot=sum(s[7])
    caps=[]
    if s[5] and s[5]<3000: caps.append("resolution below 4K")
    if s[0]=="T04": caps.append("not downloadable")
    rights=R_DEDON if s[1]=="DEDON" else R_TRIBU if s[1]=="Tribù" else R_POT
    out.append(dict(id=s[0],maker=s[1],campaign=s[2],title=s[3],file=s[4],width=s[5],height=s[6],scores=sc,total=tot,caps=caps,use=s[8],light=s[9],koda=s[10],notes=s[11],source=s[12],rights=rights,
        downloaded=bool(s[4]),medium=("Manufacturer CGI render" if s[1]=="DEDON" and s[0].startswith("D") else "Manufacturer film" if s[0].startswith("V") else "Photograph" if s[0]!="T04" else "Film (streaming)")))
out.sort(key=lambda x:-x["total"])
for i,x in enumerate(out,1): x["rank"]=i
json.dump(out,open("assets/manufacturer-source/shortlist.json","w"),indent=1)
for x in out: print(f"{x['rank']:2} {x['id']} {x['total']:3} {x['maker']:8} {x['title'][:55]:55} {x['width']}x{x['height']} {'; '.join(x['caps'])}")
