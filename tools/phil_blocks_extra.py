"""Extra product blocks for the Phil revision (merged into build_phil.BLOCKS / CLEAN on import).
Same tuple format as BLOCKS in build_phil.py; every block is 16 beats (4 bars). Plain path constants only (no import of
build_phil, which imports this module). Video in-points were checked against ffmpeg scene detection and by eye: every
clip stays inside one shot, clear of hands, people, title cards and logos.
  python3 tools/build_phil.py <cilia|tempo|clouds|totem|charlotte|mori>
Note: build_phil.block() advances its beat counter by shot[-1], which is cy (not beats) on a "full" shot that carries a cy,
so a cy is used here only on a block's last shot."""

# --- David Pompa Cilia: rapid-fire stills and light-only film moments, staggered across three pillars ---------------
CD = "src/phil/david-pompa/cilia/"; CB = CD + "brand-site/"
CF = CD + "cilia-film-capture.mov"            # Aaron's capture (768x1286): dashed selection border + handles ~8 px in
CMAT = CB + "cilia-stack_materia-mexico-milan-2025_01.mp4"           # green discs 0-1.57 | wall of discs 1.57-3.14
CCTR = CB + "cilia-stack_woven-kitchen-event_contramar-002.mp4"      # stack over the table 2.74-4.60 (person before)
CLIM = CB + "cilia_light-in-motion_specifications-davidpompa-04.mp4"  # lit stack of three once the man has left, 8.2-10.78
C003 = CB + "cilia60_davidpompa_003.mp4"      # 2400x1400: connector close-up 2.34-3.70, disc edge 7.97-10.18 (hands elsewhere)

# --- a-emotional light Tempo ----------------------------------------------------------------------------------------
TB = "src/phil/a-emotional/tempo/brand-site/"
TF = TB + "tempo_film_a-emotional-light-tempo-collection.mp4"       # shots: 0.04 4.88 8.44 12.08 15.64 19.44; logo from ~21.3
TAM = "tempo-andante_a-emotional-light-tempo-TEAN04-"; TVI = "tempo-vivace_a-emotional-light-tempo-TEVI04-"

# --- a-emotional light Clouds (LuminAir bar, DoubleTree by Hilton Amsterdam) ---------------------------------------
KD = "src/phil/a-emotional/clouds/brand-site/clouds-installation_"
KV3 = KD + "luminair-bar-hilton-amsterdam_video3.mp4"   # one continuous empty-bar walk-through (fade to white + logo from 65 s)
KV4 = KD + "luminair-bar-hilton-amsterdam_video4.mp4"   # fit-out film, empty bar; contractor logo from 55.8 s
KB1 = KD + "bretema-luminair-clip.mp4"                  # colour-changing cloud, letterboxed 1920x996; opening wipe 0-0.3 s
KB2 = KD + "bretema-luminair-clip2.mp4"                 # long table under the cloud, pillarboxed 1620x1080

# --- Pablo Totem ----------------------------------------------------------------------------------------------------
PB = "src/phil/pablo/totem/brand-site/"
PF = PB + "totem-pendant_pablo-designs_product-film_1080p.mp4"   # titles 0-11, "...GLASS" text 17-19, captions 35-37 / 49-51, end cards 73+
PIS = PB + "totem-pendant_Totem_Pendant-In-Situ-"; PDN = PB + "totem-pendant-downlight-variant_Totem_Down_"

# --- MUG Charlotte (renders + lit studio shots) ---------------------------------------------------------------------
MG = "src/phil/mug/charlotte/brand-site/mug-milano_charlotte"

# --- RBW Mori -------------------------------------------------------------------------------------------------------
RM = "src/phil/rbw/mori/"; RB = RM + "brand-site/rbw_mori"

CLEAN_EXTRA = {
    CF: "crop=748:1266:10:10",        # strip the capture's dashed border and corner/edge handles
    KB1: "crop=1916:990:2:45",        # strip letterbox bars
    KB2: "crop=1612:1076:154:2",      # strip pillarbox bars
}

EXTRA = {
  "cilia": ("David Pompa", "Cilia", [                              # Aaron: "montage images rapid fire"
    ("pillars", [
      [(CF, 23.545, 1),                                             # upper disc glowing (hard cut in at 23.533; hand enters 24.08)
       (CD + "cilia-08.png", 0, 2, 0.6), (C003, 2.40, 2, 0.57),     # arched room | connector close-up (film)
       (CB + "cilia-stack_materia-mexico-milan-2025_12.jpg", 0, 2, 0.1),
       (CB + "cilia60-double_davidpompa-002.jpg", 0, 2, 0.4), (CMAT, 1.62, 2),   # four discs over dining | wall of discs (film)
       (CB + "cilia60_davidpompa_002.jpg", 0, 2, 0.3), (CF, 27.15, 3)],          # disc and orange panel | warm disc edges (film)
      [(CMAT, 0.03, 2, 0.3), (CD + "cilia-12.png", 0, 2),           # green discs swinging (film) | pair on black
       (CB + "cilia60-double_featured-AH-project_01_photo-Studio-davidpompa.jpg", 0, 2, 0.5),
       (CLIM, 8.30, 2, 0.3), (CD + "cilia-07.jpg", 0, 2),           # lit stack of three (film) | woven texture
       (CB + "cilia60-double_featured-Brdr-Kruger-flagship_02_photo-Anders-Schonneman_stylist-Nathalie-Schwer.jpg", 0, 2, 0.2),
       (CD + "cilia-04.png", 0, 2, 0.6), (CB + "cilia60-double_davidpompa-003.jpg", 0, 2)],
      [(CCTR, 2.80, 3, 0.4), (CD + "cilia-03.jpg", 0, 2),           # Woven Kitchen stack (film) | shade detail
       (CF, 26.35, 1), (C003, 8.02, 3, 0.65),                       # both discs glowing (hand gone by 26.3) | disc edge (film)
       (CB + "cilia60-double_featured-Woven-Kitchen_03_photo-Studio-davidpompa.jpg", 0, 2, 0.3),
       (CB + "cilia60_davidpompa_003.jpg", 0, 2), (CD + "cilia-10.png", 0, 3)]], 16)]),
  "tempo": ("a-emotional light", "Tempo", [
    ("full", TB + TVI + "ambience-1.jpg", 0, 4),             # Aaron's favourite: dining by the misty valley window
    ("full", TF, 8.60, 2),                                          # film: pleats close up (shot 8.44-12.08)
    ("full", TB + TAM + "product-1.jpg", 0, 3),                # Aaron's favourite: dark room, pleat shadows on the walls
    ("pillars", [                                                   # dark trio, then a left-to-right cascade on beats 1, 2, 3
      [(TB + TVI + "product-1_white.jpg", 0, 1, 0.45), (TB + TAM + "ambience-1.jpg", 0, 4, 0.4)],   # dark box | Andante, misty window
      [(TB + TVI + "product-2_white.jpg", 0, 2), (TB + "tempo-andante_project_2017_Croatia_Jadran_hotel_Lea_Aviani_TEAN04__01.jpg", 0, 3, 0.3)],
      [(TB + "tempo-andante-ext_a-emotional-light-tempo-TEAN04-EXT-ambience-1.jpg", 0, 3, 0.76),     # Andante outdoors at night
       (TB + "tempo-vivace_project_2021-Australia-No-92-Wine-Bar-Sydney-Glebe-by-Pattern-Studio-tempo-vivace-6.jpeg", 0, 2)]], 5),
    ("full", TF, 15.80, 2)]),                                       # film: Vivace against the dark wall (shot 15.64-19.44)
  "clouds": ("a-emotional light", "Clouds", [                     # empty-bar footage only; the party film (video1) is all guests
    ("full", KV3, 15.00, 4),                                        # walk-through: under the cloud, over the bar
    ("full", KV4, 1.36, 2),                                         # fit-out film: the round bar under the cloud (shot 1.28-2.56)
    ("pillars", [
      [(KD + "luminair-bar-hilton-amsterdam_1.png", 0, 3), (KB2, 0.5, 3)],            # lit blue/amber cloud | long table (film)
      [(KB1, 1.0, 4), (KD + "luminair-bar-hilton-amsterdam_5.jpeg", 0, 2)],           # cloud changing colour (film) | violet night
      [(KD + "luminair-bar-hilton-amsterdam_10.png", 0, 2, 0.3), (KD + "luminair-bar-hilton-amsterdam_9.png", 0, 4)]], 6),
    ("full", KV4, 47.40, 2),                                        # fit-out film: cloud over the gold bar (shot 47.32-50.60)
    ("full", KD + "luminair-bretema_5.png", 0, 2, 0.1)]),           # colour-lit cloud over the bar (cy only on a last shot: see note)
  "totem": ("Pablo", "Totem", [
    ("full", PF, 22.60, 4),                                         # film: cluster glowing on dark (shot 22.49-25.13)
    ("pillars", [
      [(PIS + "12.png", 0, 3, 0.45), (PIS + "1.png", 0, 3, 0.5), (PDN + "C_D_B_-_entry_tall_-_edit_01.jpg", 0, 2, 0.2)],
      [(PF, 12.05, 2, 0.2), (PIS + "3.png", 0, 3, 0.8), (PB + "totem-pendant_gallery-hospitality_Double_CC_Window_Bar.jpg", 0, 3, 0.2)],
      [(PDN + "DDD_-_glass_conference_space.2136_copy.jpg", 0, 4), (PIS + "9.png", 0, 4, 0.4)]], 8),
    ("full", PF, 63.10, 2),                                         # film: three over the dining table (shot 62.63-71.8)
    ("full", PIS + "11.png", 0, 2, 0.05)], "r"),                    # dark panelled wall (cy: the trio hangs at the top)
  "charlotte": ("MUG", "Charlotte", [                            # rooms carry the caption (2 bars); the lit finishes follow clean
    ("full", MG + "-ambiente-1.jpg", 0, 4),                         # lounge, four clusters
    ("full", MG + "-ambiente-3.jpg", 0, 3),                         # round table, arch
    ("full", MG + "-ambiente-dining-table.jpg", 0, 3),              # long table
    ("full", MG + "_lit-on-grey_BLACK-NICKEL.jpg", 0, 2),           # the three lit finishes, full-frame (11988 px)
    ("full", MG + "_lit-on-grey_BRONZE.jpg", 0, 2),
    ("full", MG + "_lit-on-grey_DARK-BROWN.jpg", 0, 2)]),
  "mori": ("RBW", "Mori", [
    ("full", RB + "-gourd_The-Fat-Pig-New-York_01.jpg", 0, 4), # Mori Gourd row over the bar
    ("pillars", [
      [(RM + "mori-02.jpg", 0, 3, 0.45), (RM + "mori-13.jpg", 0, 3, 0.6), (RM + "mori-12.jpg", 0, 2, 0.6)],
      [(RB + "-nut_install-carousel_likely-Zen-Den_02.jpg", 0, 2, 0.7), (RM + "mori-10.jpg", 0, 3, 0.4), (RM + "mori-14.jpg", 0, 3, 0.9)],
      [(RM + "mori-01.jpg", 0, 4, 0.4), (RB + "_office-install_collection-hero.jpg", 0, 4, 0.55)]], 8),
    ("full", RB + "-nut_Zen-Den-by-Working-Holidays-LA_01.jpg", 0, 2),
    ("full", RB + "-gourd_Working-Holiday-Silver-Lake-LA_01.jpg", 0, 2)]),
}
