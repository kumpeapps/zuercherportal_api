# zuercherportal_api
 
![PyPI - Version](https://img.shields.io/pypi/v/zuercherportal_api) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zuercherportal_api)
![PyPI - License](https://img.shields.io/pypi/l/zuercherportal_api)

## Install
```python

pip install zuercherportal_api

```

## Usage
Manually Supplied Jail Prefix:
```python
import zuercherportal_api as zuercherportal

jail_api = zuercherportal.API(jail="benton-so-ar")
inmate_data = jail_api.inmate_search()
```

Using a Jail that is in our Database:
```python
import zuercherportal_api as zuercherportal
jail_api = zuercherportal.API(jail=zuercherportal.Jails.AR.BentonCounty())
inmate_data = jail_api.inmate_search()
```

Filter The Results:
```python
import zuercherportal_api as zuercherportal
jail_api = zuercherportal.API(jail=zuercherportal.Jails.AR.BentonCounty())
inmate_data = jail_api.inmate_search(
    inmate_name="",
    race="all",
    sex="all",
    cell_block="all",
    helf_for_agency="any",
    in_custody_date="",
    records_per_page=50,
    record_start=0,
    sort_by_column="name",
    sort_descending=False,
)
```

## Current Jails in our Database
Below are the jails we currently have in our database. Please feel free to raise an issue or pull request to add additional jails. I used a script to loop thru all US counties to see if zuercher portal was in use so this should be a complete list but I could have missed some or more could have been added.

<details>
<summary><strong>Arkansas (2 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Benton | Benton County AR Jail | `benton-so-ar` | `zuercherportal.Jails.AR.BentonCounty()` |
| Pulaski | Pulaski County AR Jail | `pulaski-so-ar` | `zuercherportal.Jails.AR.PulaskiCounty()` |

</details>

<details>
<summary><strong>California (1 jail)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Sutter | Sutter County CA Jail | `sutter-so-ca` | `zuercherportal.Jails.CA.SutterCounty()` |

</details>

<details>
<summary><strong>Colorado (1 jail)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Gilpin | Gilpin County CO Jail | `gilpin-so-co` | `zuercherportal.Jails.CO.GilpinCounty()` |

</details>

<details>
<summary><strong>Georgia (6 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Catoosa | Catoosa County GA Jail | `catoosa-so-ga` | `zuercherportal.Jails.GA.CatoosaCounty()` |
| Douglas | Douglas County GA Jail | `douglas-so-ga` | `zuercherportal.Jails.GA.DouglasCounty()` |
| Floyd | Floyd County GA Jail | `floyd-so-ga` | `zuercherportal.Jails.GA.FloydCounty()` |
| Houston | Houston County GA Jail | `houston-so-ga` | `zuercherportal.Jails.GA.HoustonCounty()` |
| Lumpkin | Lumpkin County GA Jail | `lumpkin-so-ga` | `zuercherportal.Jails.GA.LumpkinCounty()` |
| Toombs | Toombs County GA Jail | `toombs-so-ga` | `zuercherportal.Jails.GA.ToombsCounty()` |

</details>

<details>
<summary><strong>Iowa (7 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Clinton | Clinton County IA Jail | `clinton-so-ia` | `zuercherportal.Jails.IA.ClintonCounty()` |
| Marshall | Marshall County IA Jail | `marshall-so-ia` | `zuercherportal.Jails.IA.MarshallCounty()` |
| Pottawattamie | Pottawattamie County IA Jail | `pottawattamie-so-ia` | `zuercherportal.Jails.IA.PottawattamieCounty()` |
| Poweshiek | Poweshiek County IA Jail | `poweshiek-so-ia` | `zuercherportal.Jails.IA.PoweshiekCounty()` |
| Wapello | Wapello County IA Jail | `wapello-so-ia` | `zuercherportal.Jails.IA.WapelloCounty()` |
| Webster | Webster County IA Jail | `webster-so-ia` | `zuercherportal.Jails.IA.WebsterCounty()` |
| Winneshiek | Winneshiek County IA Jail | `winneshiek-so-ia` | `zuercherportal.Jails.IA.WinneshiekCounty()` |

</details>

<details>
<summary><strong>Idaho (2 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Clearwater | Clearwater County ID Jail | `clearwater-so-id` | `zuercherportal.Jails.ID.ClearwaterCounty()` |
| Washington | Washington County ID Jail | `washington-so-id` | `zuercherportal.Jails.ID.WashingtonCounty()` |

</details>

<details>
<summary><strong>Illinois (3 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Iroquois | Iroquois County IL Jail | `iroquois-so-il` | `zuercherportal.Jails.IL.IroquoisCounty()` |
| Ogle | Ogle County IL Jail | `ogle-so-il` | `zuercherportal.Jails.IL.OgleCounty()` |
| Whiteside | Whiteside County IL Jail | `whiteside-so-il` | `zuercherportal.Jails.IL.WhitesideCounty()` |

</details>

<details>
<summary><strong>Indiana (2 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Marshall | Marshall County IN Jail | `marshall-so-in` | `zuercherportal.Jails.IN.MarshallCounty()` |
| Wayne | Wayne County IN Jail | `wayne-so-in` | `zuercherportal.Jails.IN.WayneCounty()` |

</details>

<details>
<summary><strong>Kansas (3 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Atchison | Atchison County KS Jail | `atchison-so-ks` | `zuercherportal.Jails.KS.AtchisonCounty()` |
| Leavenworth | Leavenworth County KS Jail | `leavenworth-so-ks` | `zuercherportal.Jails.KS.LeavenworthCounty()` |
| Linn | Linn County KS Jail | `linn-so-ks` | `zuercherportal.Jails.KS.LinnCounty()` |

</details>

<details>
<summary><strong>Louisiana (5 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Acadia Parish | Acadia Parish County LA Jail | `acadia-so-la` | `zuercherportal.Jails.LA.AcadiaParishCounty()` |
| Assumption Parish | Assumption Parish County LA Jail | `assumption-so-la` | `zuercherportal.Jails.LA.AssumptionParishCounty()` |
| Bienville Parish | Bienville Parish County LA Jail | `bienville-so-la` | `zuercherportal.Jails.LA.BienvilleParishCounty()` |
| Jackson Parish | Jackson Parish County LA Jail | `jackson-so-la` | `zuercherportal.Jails.LA.JacksonParishCounty()` |
| Lafourche Parish | Lafourche Parish County LA Jail | `lafourche-so-la` | `zuercherportal.Jails.LA.LafourcheParishCounty()` |

</details>

<details>
<summary><strong>Maine (3 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Androscoggin | Androscoggin County ME Jail | `androscoggin-so-me` | `zuercherportal.Jails.ME.AndroscogginCounty()` |
| Franklin | Franklin County ME Jail | `franklin-so-me` | `zuercherportal.Jails.ME.FranklinCounty()` |
| Lincoln | Lincoln County ME Jail | `lincoln-so-me` | `zuercherportal.Jails.ME.LincolnCounty()` |

</details>

<details>
<summary><strong>Michigan (1 jail)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Monroe | Monroe County MI Jail | `monroe-so-mi` | `zuercherportal.Jails.MI.MonroeCounty()` |

</details>

<details>
<summary><strong>Minnesota (1 jail)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Pine | Pine County MN Jail | `pine-so-mn` | `zuercherportal.Jails.MN.PineCounty()` |

</details>

<details>
<summary><strong>Missouri (2 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Bates | Bates County MO Jail | `bates-so-mo` | `zuercherportal.Jails.MO.BatesCounty()` |
| Jackson | Jackson County MO Jail | `jackson-so-mo` | `zuercherportal.Jails.MO.JacksonCounty()` |

</details>

<details>
<summary><strong>Montana (12 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Broadwater | Broadwater County MT Jail | `broadwater-so-mt` | `zuercherportal.Jails.MT.BroadwaterCounty()` |
| Carbon | Carbon County MT Jail | `carbon-so-mt` | `zuercherportal.Jails.MT.CarbonCounty()` |
| Chouteau | Chouteau County MT Jail | `chouteau-so-mt` | `zuercherportal.Jails.MT.ChouteauCounty()` |
| Gallatin | Gallatin County MT Jail | `gallatin-so-mt` | `zuercherportal.Jails.MT.GallatinCounty()` |
| Jefferson | Jefferson County MT Jail | `jefferson-so-mt` | `zuercherportal.Jails.MT.JeffersonCounty()` |
| Madison | Madison County MT Jail | `madison-so-mt` | `zuercherportal.Jails.MT.MadisonCounty()` |
| Meagher | Meagher County MT Jail | `meagher-so-mt` | `zuercherportal.Jails.MT.MeagherCounty()` |
| Ravalli | Ravalli County MT Jail | `ravalli-so-mt` | `zuercherportal.Jails.MT.RavalliCounty()` |
| Roosevelt | Roosevelt County MT Jail | `roosevelt-so-mt` | `zuercherportal.Jails.MT.RooseveltCounty()` |
| Rosebud | Rosebud County MT Jail | `rosebud-so-mt` | `zuercherportal.Jails.MT.RosebudCounty()` |
| Stillwater | Stillwater County MT Jail | `stillwater-so-mt` | `zuercherportal.Jails.MT.StillwaterCounty()` |
| Valley | Valley County MT Jail | `valley-so-mt` | `zuercherportal.Jails.MT.ValleyCounty()` |

</details>

<details>
<summary><strong>North Carolina (5 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Brunswick | Brunswick County NC Jail | `brunswick-so-nc` | `zuercherportal.Jails.NC.BrunswickCounty()` |
| Davie | Davie County NC Jail | `davie-so-nc` | `zuercherportal.Jails.NC.DavieCounty()` |
| Hoke | Hoke County NC Jail | `hoke-so-nc` | `zuercherportal.Jails.NC.HokeCounty()` |
| Pender | Pender County NC Jail | `pender-so-nc` | `zuercherportal.Jails.NC.PenderCounty()` |
| Rutherford | Rutherford County NC Jail | `rutherford-so-nc` | `zuercherportal.Jails.NC.RutherfordCounty()` |

</details>

<details>
<summary><strong>North Dakota (1 jail)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Williams | Williams County ND Jail | `williams-so-nd` | `zuercherportal.Jails.ND.WilliamsCounty()` |

</details>

<details>
<summary><strong>Nebraska (2 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Johnson | Johnson County NE Jail | `johnson-so-ne` | `zuercherportal.Jails.NE.JohnsonCounty()` |
| Perkins | Perkins County NE Jail | `perkins-so-ne` | `zuercherportal.Jails.NE.PerkinsCounty()` |

</details>

<details>
<summary><strong>New Hampshire (1 jail)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Rockingham | Rockingham County NH Jail | `rockingham-so-nh` | `zuercherportal.Jails.NH.RockinghamCounty()` |

</details>

<details>
<summary><strong>New Mexico (1 jail)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Hidalgo | Hidalgo County NM Jail | `hidalgo-so-nm` | `zuercherportal.Jails.NM.HidalgoCounty()` |

</details>

<details>
<summary><strong>Ohio (12 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Ashland | Ashland County OH Jail | `ashland-so-oh` | `zuercherportal.Jails.OH.AshlandCounty()` |
| Athens | Athens County OH Jail | `athens-so-oh` | `zuercherportal.Jails.OH.AthensCounty()` |
| Fayette | Fayette County OH Jail | `fayette-so-oh` | `zuercherportal.Jails.OH.FayetteCounty()` |
| Marion | Marion County OH Jail | `marion-so-oh` | `zuercherportal.Jails.OH.MarionCounty()` |
| Medina | Medina County OH Jail | `medina-so-oh` | `zuercherportal.Jails.OH.MedinaCounty()` |
| Paulding | Paulding County OH Jail | `paulding-so-oh` | `zuercherportal.Jails.OH.PauldingCounty()` |
| Pickaway | Pickaway County OH Jail | `pickaway-so-oh` | `zuercherportal.Jails.OH.PickawayCounty()` |
| Pike | Pike County OH Jail | `pike-so-oh` | `zuercherportal.Jails.OH.PikeCounty()` |
| Preble | Preble County OH Jail | `preble-so-oh` | `zuercherportal.Jails.OH.PrebleCounty()` |
| Ross | Ross County OH Jail | `ross-so-oh` | `zuercherportal.Jails.OH.RossCounty()` |
| Scioto | Scioto County OH Jail | `scioto-so-oh` | `zuercherportal.Jails.OH.SciotoCounty()` |
| Shelby | Shelby County OH Jail | `shelby-so-oh` | `zuercherportal.Jails.OH.ShelbyCounty()` |

</details>

<details>
<summary><strong>Oklahoma (1 jail)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Cleveland | Cleveland County OK Jail | `cleveland-so-ok` | `zuercherportal.Jails.OK.ClevelandCounty()` |

</details>

<details>
<summary><strong>Oregon (1 jail)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Clatsop | Clatsop County OR Jail | `clatsop-so-or` | `zuercherportal.Jails.OR.ClatsopCounty()` |

</details>

<details>
<summary><strong>South Carolina (8 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Anderson | Anderson County SC Jail | `anderson-so-sc` | `zuercherportal.Jails.SC.AndersonCounty()` |
| Cherokee | Cherokee County SC Jail | `cherokee-so-sc` | `zuercherportal.Jails.SC.CherokeeCounty()` |
| Colleton | Colleton County SC Jail | `colleton-so-sc` | `zuercherportal.Jails.SC.ColletonCounty()` |
| Kershaw | Kershaw County SC Jail | `kershaw-so-sc` | `zuercherportal.Jails.SC.KershawCounty()` |
| Oconee | Oconee County SC Jail | `oconee-so-sc` | `zuercherportal.Jails.SC.OconeeCounty()` |
| Pickens | Pickens County SC Jail | `pickens-so-sc` | `zuercherportal.Jails.SC.PickensCounty()` |
| Union | Union County SC Jail | `union-so-sc` | `zuercherportal.Jails.SC.UnionCounty()` |
| Williamsburg | Williamsburg County SC Jail | `williamsburg-so-sc` | `zuercherportal.Jails.SC.WilliamsburgCounty()` |

</details>

<details>
<summary><strong>South Dakota (15 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Bennett | Bennett County SD Jail | `bennett-so-sd` | `zuercherportal.Jails.SD.BennettCounty()` |
| Clay | Clay County SD Jail | `clay-so-sd` | `zuercherportal.Jails.SD.ClayCounty()` |
| Custer | Custer County SD Jail | `custer-so-sd` | `zuercherportal.Jails.SD.CusterCounty()` |
| Davison | Davison County SD Jail | `davison-so-sd` | `zuercherportal.Jails.SD.DavisonCounty()` |
| Lake | Lake County SD Jail | `lake-so-sd` | `zuercherportal.Jails.SD.LakeCounty()` |
| Lawrence | Lawrence County SD Jail | `lawrence-so-sd` | `zuercherportal.Jails.SD.LawrenceCounty()` |
| Lincoln | Lincoln County SD Jail | `lincoln-so-sd` | `zuercherportal.Jails.SD.LincolnCounty()` |
| Lyman | Lyman County SD Jail | `lyman-so-sd` | `zuercherportal.Jails.SD.LymanCounty()` |
| Marshall | Marshall County SD Jail | `marshall-so-sd` | `zuercherportal.Jails.SD.MarshallCounty()` |
| Meade | Meade County SD Jail | `meade-so-sd` | `zuercherportal.Jails.SD.MeadeCounty()` |
| Pennington | Pennington County SD Jail | `pennington-so-sd` | `zuercherportal.Jails.SD.PenningtonCounty()` |
| Roberts | Roberts County SD Jail | `roberts-so-sd` | `zuercherportal.Jails.SD.RobertsCounty()` |
| Sully | Sully County SD Jail | `sully-so-sd` | `zuercherportal.Jails.SD.SullyCounty()` |
| Union | Union County SD Jail | `union-so-sd` | `zuercherportal.Jails.SD.UnionCounty()` |
| Yankton | Yankton County SD Jail | `yankton-so-sd` | `zuercherportal.Jails.SD.YanktonCounty()` |

</details>

<details>
<summary><strong>Tennessee (2 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Sullivan | Sullivan County TN Jail | `sullivan-so-tn` | `zuercherportal.Jails.TN.SullivanCounty()` |
| Washington | Washington County TN Jail | `washington-so-tn` | `zuercherportal.Jails.TN.WashingtonCounty()` |

</details>

<details>
<summary><strong>Texas (3 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Brooks | Brooks County TX Jail | `brooks-so-tx` | `zuercherportal.Jails.TX.BrooksCounty()` |
| Presidio | Presidio County TX Jail | `presidio-so-tx` | `zuercherportal.Jails.TX.PresidioCounty()` |
| Upshur | Upshur County TX Jail | `upshur-so-tx` | `zuercherportal.Jails.TX.UpshurCounty()` |

</details>

<details>
<summary><strong>Virginia (2 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Caroline | Caroline County VA Jail | `caroline-so-va` | `zuercherportal.Jails.VA.CarolineCounty()` |
| Northumberland | Northumberland County VA Jail | `northumberland-so-va` | `zuercherportal.Jails.VA.NorthumberlandCounty()` |

</details>

<details>
<summary><strong>Wisconsin (6 jails)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Dunn | Dunn County WI Jail | `dunn-so-wi` | `zuercherportal.Jails.WI.DunnCounty()` |
| Grant | Grant County WI Jail | `grant-so-wi` | `zuercherportal.Jails.WI.GrantCounty()` |
| Lincoln | Lincoln County WI Jail | `lincoln-so-wi` | `zuercherportal.Jails.WI.LincolnCounty()` |
| Menominee | Menominee County WI Jail | `menominee-so-wi` | `zuercherportal.Jails.WI.MenomineeCounty()` |
| Monroe | Monroe County WI Jail | `monroe-so-wi` | `zuercherportal.Jails.WI.MonroeCounty()` |
| Washburn | Washburn County WI Jail | `washburn-so-wi` | `zuercherportal.Jails.WI.WashburnCounty()` |

</details>

<details>
<summary><strong>Wyoming (1 jail)</strong></summary>

| County | Jail Name | Jail ID | Class Access |
|--------|-----------|---------|--------------|
| Teton | Teton County WY Jail | `teton-so-wy` | `zuercherportal.Jails.WY.TetonCounty()` |

</details>

