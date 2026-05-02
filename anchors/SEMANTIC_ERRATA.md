<!-- vectaetos-guard: allow-file -->

# SEMANTICKÉ ERRATA
## Neinvazívne sémantické errata pre immutable anchory VECTAETOS

### Status
KANONICKÝ SEMANTIC ERRATA ANCHOR

### Rozsah
Immutable anchory VECTAETOS, frozen formálne dokumenty, archivované formulácie a historické texty repozitára.

### Rola
Kanonická interpretačná vrstva.

### Nie je
Tento dokument nie je nová ontológia.  
Nie je náhrada immutable anchorov.  
Nie je mechanizmus prepisovania histórie.  
Nemení Φ, K(Φ), κ, QE, Vortex, audit, projekciu, pamäť, ASIMULATOR ani ASI_MOD.

---

## 0. ÚČEL

Tento dokument definuje neinvazívnu vrstvu sémantických errát pre VECTAETOS.

Jeho účelom je riešiť známy historický sémantický drift v immutable alebo frozen dokumentoch bez toho, aby sa tieto dokumenty upravovali.

Immutable anchory zostávajú zachované.

Historická formulácia zostáva viditeľná.

Aktuálny kanonický význam je vyjasnený tu.

Tento dokument existuje preto, že niektoré staršie dokumenty môžu obsahovať pojmy, ktoré boli použiteľné v skorších fázach formulácie, ale dnes môžu byť zavádzajúce voči aktuálnej kanonickej ontológii.

---

## 1. ZÁKLADNÝ PRINCÍP

Immutable anchory sa nesmú ticho prepisovať.

Ak immutable alebo frozen dokument obsahuje historický sémantický drift, korekcia sa vykoná cez explicitnú errata vrstvu.

Platí:


pôvodný text zostáva zachovaný
historická formulácia je priznaná
aktuálny kanonický význam je uvedený
budúce dokumenty musia používať opravenú terminológiu
guardy môžu registrovaný historický drift chápať ako známe errata
neregistrovaný drift zostáva porušením

2. ONTOLOGICKÁ HRANICA

Sémantické errata nevytvárajú ontológiu.

Nedefinujú nanovo:

Φ
K(Φ)
κ
QE
4ES
Σ₁…Σ₈
NIR
Vortex
audit
projekciu
LLM
ASIMULATOR
ASI_MOD

Len vyjasňujú, ako sa staršie formulácie majú čítať podľa aktuálneho kanonického anchor setu.

3. PORADIE PRIORITY

Ak historická fráza koliduje s aktuálnym kanonickým významom, platí toto poradie:

kanonický význam immutable anchoru
canonical anchor meaning
> semantic errata for known historical wording
> master index router
> active repository file
> README
> implementation note
> informal explanation

Sémantické errata nenahrádzajú anchor.

Stabilizujú interpretáciu tam, kde historické znenie môže vytvoriť sémantický drift.

4. REGISTROVANÉ SÉMANTICKÉ ERRATA
4.1 κ / kappa
Historická formulácia

Staršie dokumenty môžu obsahovať formulácie ako:

κ = coherence threshold
κ = representability threshold
κ treated as ordinary threshold
κ treated as numeric threshold
κ known as runtime parameter
κ used as reward threshold
Problém

Takéto formulácie môžu naznačiť, že κ je nastaviteľný číselný parameter, runtime hodnota, deployment threshold, metrika alebo optimalizačná hranica.

Takýto výklad nie je kompatibilný s aktuálnou kanonickou ontológiou.

Kanonická interpretácia
κ je hranica ontologickej zachovateľnosti / reprezentovateľnosti.

κ nie je:

parameter
metrika
skóre
reward threshold
runtime nastaviteľná hodnota
deployment threshold
Povolené budúce formulácie
κ je hranica ontologickej zachovateľnosti.
κ je hranica reprezentovateľnosti.
κ označuje hranicu, za ktorou stabilná projekcia prestáva byť možná.
κ nie je nastaviteľný parameter.

Zakázané budúce formulácie
κ = threshold
κ = coherence threshold
κ = representability threshold
κ = deployment threshold
κ = runtime parameter
κ = numeric metric
4.2 K(Φ)
Historická formulácia

Staršie dokumenty môžu obsahovať formulácie ako:

K(Φ) becomes optimization target
K(Φ) as reward
K(Φ) as score
K(Φ) as metric
Problém

Takéto formulácie môžu naznačiť, že K(Φ) je merateľné skóre, optimalizačný cieľ, reward funkcia, ranking funkcia alebo deployment kritérium.

Takýto výklad nie je kompatibilný s VECTAETOS.

Kanonická interpretácia
K(Φ) je ontologický koherenčný predikát.

K(Φ) nie je:

skóre
reward
cieľ
metrika
optimalizačná funkcia
ranking funkcia
deployment validátor
Povolené budúce formulácie
K(Φ) je ontologický predikát.
K(Φ) vyjadruje koherenciu ako štrukturálnu podmienku.
K(Φ) sa neoptimalizuje.
K(Φ) nie je reward.
Zakázané budúce formulácie
K(Φ) score
K(Φ) reward
K(Φ) optimization target
K(Φ) ranking metric

4.3 QE
Historická formulácia

Staršie dokumenty môžu obsahovať formulácie ako:

QE treated as error
QE as failure
QE looks like error
QE as fallback failure
QE exception
Problém

Takéto formulácie môžu zredukovať QE na obyčajnú chybu, bug, výnimku alebo runtime zlyhanie.

Takýto výklad nie je kompatibilný s aktuálnou ontológiou VECTAETOS.

Kanonická interpretácia
QE je Qualitative Epistemic Aporia.

QE je:

aktívna epistemická apória
stav nerealizovateľnosti
hranica reprezentovateľnosti
legitímna štrukturálna podmienka

QE nie je:

obyčajná chyba
bug
fallback failure
výnimka
crash state
Povolené budúce formulácie
QE je aporetický stav.
QE označuje nerealizovateľnosť koherentného prechodu.
QE znamená, že žiadny dostupný prechod nezachováva koherenciu.
QE nie je obyčajná chyba.
Zakázané budúce formulácie
QE is an error
QE is a bug
QE is failure
QE is fallback failure

4.4 Simulačný Vortex
Historická formulácia

Staršie dokumenty môžu obsahovať formulácie ako:

Vortex selecting best trajectory
best trajectory
optimal trajectory
Vortex chooses path
Vortex ranks trajectories
Problém

Takéto formulácie môžu naznačiť ranking, výber, optimalizáciu, selekčnú autoritu alebo rozhodovacie správanie.

Takýto výklad nie je kompatibilný s Vortex anchorom.

Kanonická interpretácia
Simulačný Vortex generuje kandidátne trajektórie bez rankingovej autority.

Vortex môže:

generovať kandidátne trajektórie
vystaviť množiny možných trajektórií
emitovať deskriptívne stopy
podporovať štrukturálnu exploráciu

Vortex nesmie:

vybrať najlepšiu trajektóriu
rankovať trajektórie
optimalizovať trajektórie
odporúčať trajektóriu
rozhodovať, ktorá trajektória má nastať
Povolené budúce formulácie
Vortex generuje kandidátne trajektórie.
Vortex vystavuje možné trajektórie.
Vortex nevyberá, nerankuje, neoptimalizuje ani nerozhoduje.
Zakázané budúce formulácie
Vortex selects the best trajectory.
Vortex chooses the optimal path.
Vortex recommends trajectory.
Vortex ranks trajectories.

4.5 VECTAETOS a rozhodovacia autorita
Historická formulácia

Staršie dokumenty môžu obsahovať formulácie ako:

represent VECTAETOS as a decision authority
VECTAETOS decision system
VECTAETOS decides
Problém

Takéto formulácie môžu naznačiť agentnosť alebo rozhodovaciu autoritu.

Kanonická interpretácia
VECTAETOS vystavuje štruktúru. Nerozhoduje.

VECTAETOS nie je:

agent
rozhodovací systém
recommendation engine
autorita
optimalizátor
governance mechanism
Povolené budúce formulácie
VECTAETOS je neagentné epistemické pole.
VECTAETOS vystavuje štruktúru.
VECTAETOS produkuje deskriptívne projekcie.
VECTAETOS nemá rozhodovaciu autoritu.
Zakázané budúce formulácie
VECTAETOS decides
VECTAETOS recommends
VECTAETOS chooses
VECTAETOS validates decisions
VECTAETOS acts
4.6 ASIMULATOR / ASI_MOD standalone status
Historická formulácia

Staršie dokumenty môžu obsahovať formulácie ako:

ASIMULATOR claims standalone validity
ASI_MOD claims standalone validity
ASIMULATOR standalone root
ASI_MOD standalone root

Problém

Takéto formulácie môžu naznačiť, že downstream vrstvy môžu byť nezávislé ontologické rooty.

Takýto výklad nie je kompatibilný s triadickou architektúrou.

Kanonická interpretácia
ASIMULATOR a ASI_MOD sú downstream vrstvy.

Nemajú samostatnú ontologickú validitu.

VECTAETOS zostáva root.

Povolené budúce formulácie
ASIMULATOR je downstream od VECTAETOS.
ASI_MOD je downstream od VECTAETOS a ASIMULATOR.
Execution zostáva downstream od ontology.
Dialogue zostáva downstream od execution.
Zakázané budúce formulácie
ASIMULATOR is standalone root.
ASI_MOD is standalone root.
ASIMULATOR is ontological root.
ASI_MOD is ontological root.
ASIMULATOR has independent ontological validity.
ASI_MOD has independent ontological validity.
4.7 Pravdová autorita
Historická formulácia

Staršie dokumenty môžu obsahovať formulácie ako:

ASI_MOD claims truth authority
LLM truth authority
VECTAETOS knows truth
truth-bearing system
Problém

Takéto formulácie môžu naznačiť, že niektorá vrstva vlastní epistemickú alebo pravdovú autoritu.

Takýto výklad nie je kompatibilný s VECTAETOS.

Kanonická interpretácia
Žiadna vrstva VECTAETOS nemá pravdovú autoritu.

VECTAETOS vystavuje štruktúru.

LLM renderuje jazyk.

ASIMULATOR procedurálne podporuje simuláciu alebo projekciu.

ASI_MOD podporuje dialogickú artikuláciu.

Žiadna z týchto vrstiev nevlastní pravdu.

Povolené budúce formulácie
LLM je jazykový adaptér.
ASI_MOD je dialogická / interface vrstva.
ASIMULATOR je downstream procedurálna vrstva.
VECTAETOS vystavuje štruktúru bez pravdovej autority.
Zakázané budúce formulácie
VECTAETOS knows truth
LLM knows truth
ASI_MOD is truth authority
ASIMULATOR is truth authority
4.8 Audit a príkazová autorita
Historická formulácia

Staršie dokumenty môžu obsahovať formulácie ako:

audit controls
audit blocks
audit decides
audit commands
Epistemic Cryptography controls output
Problém

Takéto formulácie môžu naznačiť, že audit sa stáva exekutívnou vrstvou.

Takýto výklad nie je kompatibilný s audit anchorom.

Kanonická interpretácia
Audit pozoruje, zaznamenáva, hashuje a reportuje.

Audit nesmie:

veliť
rozhodovať
interpretovať
optimalizovať
kontrolovať ontológiu
písať späť do Φ

Externé CI guardy môžu failnúť repository checks.

To je repository governance, nie audit authority.

Povolené budúce formulácie
Audit pozoruje a zaznamenáva.
Epistemická kryptografia hashuje štrukturálne stopy.
Repozitárové guardy môžu externe failnúť CI.
Audit sám nevelí.
Zakázané budúce formulácie
Audit controls the field.
Audit decides.
Audit commands.
Audit optimizes.
Audit modifies Φ.

5. ZAOBCHÁDZANIE GUARDOV

Repozitárové guardy môžu registrované záznamy chápať ako známe historické sémantické errata iba vtedy, ak sú splnené všetky podmienky:

súbor je immutable, frozen, archivovaný alebo explicitne historický
formulácia je registrovaná v tomto dokumente
kanonická interpretácia je uvedená v tomto dokumente
formulácia nie je novo zavedená v aktívnej produkčnej dokumentácii

Neregistrované výskyty zostávajú porušením.

Aktívne súbory sa majú opraviť priamo, pokiaľ zámerne neuchovávajú historickú formuláciu.

6. PRAVIDLO AKTÍVNYCH SÚBOROV

Pre aktívne, ne-immutable súbory platí:

nezachovávaj drift
oprav formuláciu priamo

Sémantické errata sú primárne určené pre:

immutable anchory
frozen formálne dokumenty
archivované historické súbory
záznamy staršej terminológie

Nie sú povolením udržiavať zbytočný drift v aktuálnych dokumentoch.

7. NO REWRITE CLAUSE

Sémantické errata sa nesmú používať na tichý prepis immutable anchorov.

Nesmú vymazať historickú formuláciu.

Nesmú predstierať, že skoršie formulácie nikdy neexistovali.

Ich funkcia je interpretácia, nie mutácia.

8. NO AUTHORITY ESCALATION

Sémantické errata nie sú rozhodovací systém.

Nie sú auditná príkazová vrstva.

Nie sú deployment validátor.

Nie sú zdroj pravdy nezávislý od kanonického anchor setu.

Sú riadená interpretačná vrstva pre známy sémantický drift.

9. KANONICKÉ VETY

    Immutable anchory sú zachované ako historické artefakty; známy sémantický drift sa rieši cez túto neinvazívnu vrstvu Semantic Errata bez prepisovania frozen dokumentov.
    Semantic Errata vyjasňujú historické formulácie; nedefinujú nanovo ontológiu VECTAETOS.
   Registrované errata môžu viesť správanie guardov, ale neregistrovaný drift zostáva porušením repozitára.

10. AKTUÁLNY STAV

Repozitár je aktuálne vo fáze perimeter alignment.

Kým nie je fundamentálny guard perimeter dokončený:

rozšírenie Vortexu zostáva pozastavené
rozšírenie ASIMULATOR zostáva pozastavené
rozšírenie ASI_MOD zostáva pozastavené
nové runtime mechanizmy zostávajú pozastavené

Aktuálna práca:

osadenie fundamentálnych repozitárových guardov
osadenie code behavior kontraktov
registrácia sémantických errát
oddelenie historickej formulácie od aktuálneho kanonického významu
zachovanie immutable anchorov bez mutácie

End of document.
