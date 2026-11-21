# Version 2: KODA lighting placement recommendations

Only fixtures in KODA's current range (kodalighting.com product feeds, downloaded 20 November) are proposed. Heights and colour temperatures are working assumptions to check against each data sheet before any composite is called accurate.

| Scene | Environment | Fixture | Placement | Light behaviour to match |
|---|---|---|---|---|
| D04 | Pergola dining by the river (DEDON Spiritual Mountain) | Occhio Mito sospeso 60, bronze, two units; or Lodes Volum, three globes | Hung from the pergola beams on the table's long axis, about 75 cm above the top | 2700 K pool on the table, soft falloff onto the chairs, bronze ring catching the dusk sky; the two DEDON table lamps dim back |
| D03 | Mountain terrace lounge at dusk (DEDON Mu Mystique) | Occhio Mito largo, arc floor light | Base behind the sofa's left arm, ring over the coffee table | Downward ring light on the table and rug; the fireplace stays the warm accent |
| D01 | Lake house at night (DEDON Secret Lakeside) | Arkoslight trimless downlights (Black Foster family) | Deck soffit and the stone-wing eaves | Narrow beams grazing the stone and timber; the reflection doubles them in the lake |
| D02 | Cliff villa at blue hour (DEDON Mysterious Desert) | Arkoslight recessed linear; A-N-D Column pendants | Linear in the cantilever soffit; Column over the lower terrace seating | Long soffit wash defining the cantilever; the interior is already lit in the source |
| D05 | Canyon pavilion | A-N-D Pace pendants; Arkoslight step lights | Pace in the pavilion bay; step lights along the water deck | Warm interior glow against the cooling canyon |
| D06 | Stone lake house terrace | Pablo Bola felt pendants; Occhio wall lights | Bola under the eaves over the lounge; wall lights on the stone piers | Diffuse felt glow and grazing light on stone |
| P01 | Izar Houses long dining hall (Potocco project) | Lodes Random cluster, or A-N-D Pebble linear | Centred over the long table, replacing the small table lamps | The hall's existing cove light stays; the pendants add the focal pool |
| P02 | Hotel Ansitz Steinbock lounge (Potocco project) | Occhio Luna sospeso cloud, or A-N-D Vale chandelier | In place of the existing pendant | Low, warm sphere light against the vaulted plaster |

**Method, as tested.**

- **"Lights off" plate.** `tools/lightsoff.py` finds the light already in a render (bright and warm, or pool light), pulls each source down to the ambient around it while keeping its texture, removes its warm spill, and drops the ambient by about a stop. The original image is the "on" state.
  - Tested on D01: the result is believable.
  - Tested on D02: the large glazing leaves pale patches, so it needs a hand-cut window mask.
- **KODA fixtures.** These go in as the manufacturer's own transparent product cut-outs, the method Version 1 used. Each gets its own glow, a pool of light on the surface below, and a shadow, scaled from the furniture in the frame.

**Conflicting fittings.** DEDON makes its own lanterns (The Others, Dala, Scoora), and they light several of the strongest scenes (D03, D05, D06, D08, D11). Each composite can do one of two things:

- dim them back so KODA leads, or
- leave them, if DEDON should be seen as part of the partnership.
