# RKIC-SITE Project — Claude ki Galtiyon ka Record

*Rahul Kejriwal ke liye, is project ki poori history se, imaandaari se compile kiya gaya. Kisi bhi cheez ko chhupaya ya halka karke nahi likha gaya hai.*

## Baar-baar dohraayi gayi galtiyan (ek hi issue kai baar report karwana pada)

**1. Header tagline "· EST. 1999" wrap (12 Sep 2026) — 2 round**
- Round 1: Rahul ne screenshot bhej kar bataya ki tagline mobile par ajeeb tarike se toot rahi hai ("estd 1999 uppar niche"). Maine font-size/letter-spacing kam karne ki koshish ki, phir usko revert kiya, phir `&nbsp;` ka istemaal karke ek "clean 2-line wrap" banaya — lekin yeh Rahul ka asli maang samjhe bina hi shipped kar diya.
- Round 2: Rahul ne 3 phone screenshots bheje, wahi problem abhi bhi dikh rahi thi. Usne bahut gussa ho kar bataya ki maine galat cheez fix ki — usko koi bhi wrap nahi chahiye tha, sirf 1 line chahiye thi, "clean 2-line" nahi. Tabhi jaakar maine sahi sawal poocha aur sahi fix (EST. 1999 poori tarah hatana) kiya.
- **Meri galti**: uski shuruaati baat ko sahi se nahi samjha, apni taraf se ek "behtar" lekin galat solution bana diya.

**2. Mobile drawer/menu — 3 round**
- Round 1: Drawer poore screen ko cover kar raha tha (header ke neeche se khulna chahiye tha) + apna alag branding block tha jo header ki company details se duplicate ho raha tha. Dono fix kiye.
- Round 2: Rahul ne bataya "breadcrumb par tap karne se drawer band nahi hota" — maine sirf "outside click" wala fix diya jo kaafi nahi tha.
- Round 3: Wahi problem phir se report hui — drawer full-width hone ki wajah se "bahar" koi jagah thi hi nahi tap karne ke liye. Tab jaake andar ki khaali jagah tap karne se bhi close hone wala fix kiya.
- **Meri galti**: pehli baar mein hi poori tarah root-cause nahi socha, ek partial fix diya jo dobara toot gaya.

**3. Theme (rang) mismatch — 2 round**
- Round 1 (11 Sep): forest-green theme laga di, phir Rahul ke kehne par purani slate-blue/gold theme par wapas laaya — lekin yeh revert sirf index.html aur 9 product pages par hi hua, baaki 127 pages chhoot gaye.
- Round 2 (12 Sep): Rahul ne 3 screenshots + video bhej kar bataya ki "company details mismatch" ho rahi hai — tab jaake pata chala ki 127 pages abhi bhi purani (forest-green) theme par hi hain. Sabhi 127 fix kiye.
- **Meri galti**: batch-fix ko "sabhi files" manaa, lekin actual scope kabhi poori tarah verify nahi kiya — partial file listing se scope decide kiya, poori directory scan nahi ki.

**4. Photo-zoom / magnifying-glass feature — kai round, aakhir mein poori tarah hataani padi (band ki gayi 8 Sep 2026)**
Product photo par zoom/magnify karne wala feature real mobile device par hang ho jaata tha. Maine isko theek karne ki kai alag-alag koshishein ki — base64 data size kam karna, brandLogos handling badalna, render-blocking scripts hatana, cache-busting lagana, touch-action:manipulation add karna — har baar laga ki fix ho gaya, lekin Rahul ke asli phone par phir se hang ho jaata tha. Kai round fail hone ke baad, akhir mein feature ko poori site se (index.html + sabhi standalone pages) hamesha ke liye hata diya — matlab maine problem "solve" nahi ki, sirf usse bachne ka rasta chuna.
**Meri galti**: shuru se hi is tarah ke touch/gesture bugs sirf screenshot/desktop-emulation se pakde nahi jaate — asli device par baar-baar test kiye bina hi "fix ho gaya" maan liya, kai baar galat saabit hua.

## Bina-report-hue lekin record honi chahiye galtiyan

**5. Photo/nameplate mixup — brahma-re3-220v-c1035 (10 Sep 2026)**
Do products ke naam alag the, lekin unki photo same thi. Maine online research karke maan liya ki yeh ek plausible/normal reuse hai — lekin Rahul ne khud check kiya to pata chala ki photo mein doosre product ka nameplate code dikh raha tha, matlab yeh ek asli galti thi, sirf similar-dikhne wali stock photo nahi. Rahul ke bataane par hi pakdi gayi, maine khud nahi pakdi.

**6. products-added-list.md (changelog file) — 2 baar silently revert hui**
Dono baar file commit "successful" dikhaya, lekin kuch der baad check karne par pata chala ki file purani state par revert ho chuki thi (naye entries gayab). Dono baar dobara likh kar commit karna pada. Iska pakka root cause abhi tak pata nahi — shayad aapke system ke background auto-commit process se clash ho raha hai — lekin yeh mere liye ek blind-spot raha jab tak maine khud dobara check na kiya.

**7. GitHub push status confusion (12 Sep 2026)**
Ek fix ke baad maine bataya "device par commit ho gaya, GitHub par push nahi hua" — Rahul ne confirm kiya ki push nahi aaya. Yeh galti nahi thi (sahi diagnosis tha), lekin isne confusion aur ek extra round of back-and-forth paida kiya kyunki maine pehle spasht nahi kiya tha ki main khud GitHub par push nahi kar sakta.

**8. "Looks fine" wala shallow jawab (11 Sep 2026)**
Header/logo scale ka ek fix report karte waqt maine bina thik se verify kiye "theek lag raha hai" jaisa jawab diya. Rahul ne saaf mana kiya: "Aap AI hoke nahi deta. Aap local developer ke tarah baat na kare" — matlab bina proof/screenshot ke sirf keh dena ki kaam ho gaya, kaafi nahi tha. Uske baad Playwright se properly verify karna shuru kiya.

## Meta-pattern (asli jad ki wajah)

Zyaadatar upar ki galtiyon ke peeche ek hi common wajah hai: **sirf desktop (ya sirf ek jagah) check karke "done" bol dena**, jabki mobile par alag dikh raha hota tha — ya user ki asli maang ko poori tarah samjhe bina jaldi mein ek fix ship kar dena. Isi wajah se 12 Sep 2026 ko do standing rules banaye gaye (project memory mein save):
1. Har fix desktop AND mobile dono par ek saath verify karna, "done" bolne se pehle.
2. 136+ files par batch fix karne se pehle, aur GitHub tak pahunchne se pehle, pehle ek sample screenshot dikhana aur confirmation lena.

---
*Yeh document is session ki project-memory history se compile kiya gaya hai — koi bhi purani session/chat jiska record memory mein save nahi hai, usme aur bhi galtiyan hui ho sakti hain jo yahan list nahi hain.*
