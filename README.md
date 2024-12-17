# File-Manager-Arka

**Proiect pentru materia de la Universitatea "Dunărea de Jos din Galați"**

File-Manager-Arka este un manager de fișiere simplu, similar unui File Explorer, aflat în stadiu demo. Acest proiect oferă trei funcționalități principale:

1. **Convertirea fișierelor** (audio, video și imagini)  
   *În viitor, va include și documente.*
2. **Descărcarea conținutului audio sau video** de pe pagini web precum YouTube, Soundcloud etc.
3. **Criptarea și decriptarea fișierelor**  
   *În curând, va fi disponibilă și opțiunea de protecție cu parolă pentru o securitate mai sporită.*

---

## Cerințe

Pentru a utiliza acest proiect, este necesar să aveți **Python** instalat pe sistemul dumneavoastră și să activați un mediu virtual (**virtual environment**) pentru gestionarea librăriilor necesare.

De asemenea, pentru funcționalitatea de conversie a fișierelor audio/video, este necesară instalarea **FFmpeg**.


## Instalare și configurare

### 1. Configurarea mediului virtual

Accesați directorul proiectului și rulați următoarele comenzi în **Command Prompt** (CMD):

```cmd
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

> **Notă**: Recomandăm folosirea CMD în loc de PowerShell, deoarece anumite comenzi pot genera erori în PowerShell.

### 2. Dezactivarea mediului virtual

După ce ați terminat de utilizat proiectul, pentru a dezactiva mediul virtual, rulați:

```cmd
.venv\Scripts\deactivate.bat
```

### 3. Instalarea FFmpeg

Pentru funcționalitatea de conversie, descărcați **FFmpeg** de la următorul link:

- [Pagina oficială FFmpeg](https://www.ffmpeg.org/download.html)

**Instrucțiuni FFmpeg:**
- După descărcare, plasați folderul FFmpeg în directorul `File-Manager-Arka`.
- Astfel, calea necesară va fi preluată automat (fără a fi nevoie să o setați la nivel de sistem).

---

## Funcționalități

### Convertirea fișierelor
- Convertirea fișierelor **audio**, **video** și **imagini** între diverse formate.
- Extinderi viitoare pentru documente.

### Descărcarea conținutului de pe web
- Descărcarea fișierelor **audio** sau **video** din pagini web precum **YouTube** și **Soundcloud**.

### Criptarea și decriptarea fișierelor
- Criptarea fișierelor pentru securitate.
- În curând: protecție cu parolă pentru o dificultate sporită la accesarea fișierelor.

---

## Raportarea erorilor

Dacă întâmpinați erori în utilizarea proiectului, vă rugăm să le raportați în categoria **Issues** a repository-ului GitHub.

---

## Exemple de comenzi utile

### Activarea mediului virtual
```cmd
.venv\Scripts\activate.bat
```

### Instalarea dependențelor
```cmd
pip install -r requirements.txt
```

### Dezactivarea mediului virtual
```cmd
.venv\Scripts\deactivate.bat
```

---

## Contribuții
Contribuțiile sunt binevenite! Dacă doriți să adăugați funcționalități sau să rezolvați probleme, deschideți un **Pull Request** sau raportați erorile în secțiunea **Issues**.


---

## Contact
Pentru întrebări sau feedback legat de proiect, vă rugăm să ne contactați prin secțiunea **Issues** din repository.

---

**Mulțumim pentru utilizare și feedback!**
