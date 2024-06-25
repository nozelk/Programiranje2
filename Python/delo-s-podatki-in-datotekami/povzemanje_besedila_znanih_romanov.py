# =============================================================================
# Povzemanje besedila znanih romanov
#
# Danih je deset tekstovnih datotek z besedilom znanih romanov v angleškem jeziku.
# To so `Adventures of Huckleberry Finn`, `Alice's adventures in Wonderland`,
# `Dracula`, `Frankenstein`, `Grimms' fairy tales`, `Iliad`, `Metamorphosis`,
# `Moby Dick`, `Peter Pan` in `War and peace`. Vsako besedilo je shranjeno v
# datoteki z imenom enakim imenu romana (z malimi črkami ločenimi s podčrtajem _)
# in s končnico `txt` (npr. `war_and_peace.txt`). Datoteko zip z besedili
# dobite [tukaj](http://zaversnik.fmf.uni-lj.si/vaje/prog2-pra/besedila.zip).
# Razpakirajte si jo v isto mapo, kjer boste imeli program.
# 
# Poiskali bomo karakterističe besede oziroma termine,
# ki posamezen roman kar najbolje ločijo od ostalih romanov.
# =====================================================================@027396=
# 1. podnaloga
# Sestavite funkcijo `frekvence(naslov)`, ki vrne slovar besed z njihovimi
# frekvencami za roman shranjen v tekstovni datoteki z imenom `naslov` in
# končnico `txt`. Beseda je zaporedje znakov, sestavljeno iz črk, števk in
# podčrtajev. Vse druge znake obravnavamo kot ločila. Funkcija naj ne ločuje
# med malimi in velikimi črkami. Besede v slovarju naj bodo zapisane z malimi črkami.
# 
#     >>> frekvence('moby_dick')['whale']
#     1230
# =============================================================================
import re

def frekvence(naslov):
    s = {}
    with open("C:\\Users\\kosmr\\Desktop\\Prog 2\\delo-s-podatki-in-datotekami\\"+naslov+".txt", "r",encoding="utf-8") as dat:
        for v in dat:
            #re.split(r'\W+',v.lower()): samo sklepma da ne pisemo stavke z 2 ali vec zaporednima nealfanumerični
            for b in re.split(r'\W',v.lower()):
                if len(b) == 0:
                    continue
                s[b] = s.get(b,0) + 1
    return s
# =====================================================================@027398=
# 2. podnaloga
# Sestavite funkcijo `tf(doc)`, ki za slovar besed s frekvencami `doc`
# vrne slovar besed z izračunanimi vrednostmi metrike $\operatorname{tf}$
# (term frequency).
# $$ \operatorname{tf}(t,d)=0.5+0.5\,\frac{f(t,d)}{\max_{t'}\{f(t',d)\}} $$
# Pri tem je $f(t,d)$ frekvenca termina $t$ v besedilu $d$.
# 
#     >>> tf(frekvence('war_and_peace'))['war']
#     0.5043484521238301
# =============================================================================
def tf(doc):
    s = {}
    najvec = max(doc.values())
    for i in doc:
        s[i] = .5 + .5 * doc[i] / najvec
    return s
# =====================================================================@027399=
# 3. podnaloga
# Sestavite funkcijo `idf(docs)`, ki za slovar slovarjev besed s frekvencami
# `docs` vrne slovar besed z izračunanimi vrednostmi metrike $\operatorname{idf}$
# (inverse document frequency).
# $$ \operatorname{idf}(t,D)=\log\,\frac{|D|}{|\{d\in D:f(t,d)>0\}|} $$
# Pri tem je $f(t,d)$ frekvenca termina $t$ v besedilu $d$ in $D$ množica vseh besedil.
# 
#     >>> naslovi = ['iliad', 'moby_dick', 'war_and_peace', 'peter_pan', ...]
#     >>> docs = {naslov: frekvence(naslov) for naslov in naslovi}
#     >>> idf(docs)['blood']
#     0.22314355131420976
# =============================================================================
import math

def idf(docs):
    s = {}
    D = len(docs)
    b = set()
    for i in docs.values():
        b.update(i.keys())
    for i in b:
        st = 0
        for j in docs.values():
            if i in j:
                st += 1
        s[i] = math.log(D/st)
    return s
# =====================================================================@027400=
# 4. podnaloga
# Z uporabo zgornjih funkcij sestavite funkcijo `tfidf(naslov, docs)`,
# ki za roman z naslovom `naslov` in slovar slovarjev `docs` vrne
# slovar besed z izračunanimi vrednostmi metrike $\operatorname{tf-idf}$
# (term frequency–inverse document frequency).
# $$ \operatorname{tf-idf}(t,d,D)=\operatorname{tf}(t,d)\cdot\operatorname{idf}(t,D) $$
# 
#     >>> tfidf('iliad', docs)['trojans']
#     1.1598929846134225
# =============================================================================
def tfidf(naslov, docs):
    s = {}
    sIDF=idf(docs)
    sTF=tf(docs[naslov])
    for beseda in sTF:
        s[beseda]=sTF[beseda]*sIDF[beseda]
    return s
# =====================================================================@027401=
# 5. podnaloga
# Sestavite funkcijo `karakteristicne_besede(naslov, docs, n)`, ki za roman z
# naslovom `naslov` izpiše `n` najbolj karakterističnih besed glede na
# vrednosti metrike $\operatorname{tf-idf}$. Realna števila naj izpiše
# na 4 decimalna mesta natančno in na 6 znakov širine.
# 
#     >>> karakteristicne_besede('iliad', docs, 10)
#      Novel | 'iliad'
#     1.1847 | 'hector'
#     1.1772 | 'troy'
#     1.1679 | 'trojan'
#     1.1632 | 'ajax'
#     1.1632 | 'patroclus'
#     1.1603 | 'ulysses'
#     1.1599 | 'trojans'
#     1.1586 | 'coursers'
#     1.1584 | 'nestor'
#     1.1584 | 'priam'
# =============================================================================
def karakteristicne_besede(naslov, docs, n):
    sTFIDF = tfidf(naslov, docs)
    s = sorted(sTFIDF.items(), key=lambda x: (-x[1], x[0]))
    print(f" Novel | '{naslov}'")
    st, tmp = 0, 0
    while st < n:
        vr = s[tmp][1]
        b = s[tmp][0]
        print("{:.4f} | '{}'".format(vr, b))
        st += 1
        tmp += 1




































































































# ============================================================================@
# fmt: off
"Če vam Python sporoča, da je v tej vrstici sintaktična napaka,"
"se napaka v resnici skriva v zadnjih vrsticah vaše kode."

"Kode od tu naprej NE SPREMINJAJTE!"

# isort: off
import json
import os
import re
import shutil
import sys
import traceback
import urllib.error
import urllib.request
import io
from contextlib import contextmanager


class VisibleStringIO(io.StringIO):
    def read(self, size=None):
        x = io.StringIO.read(self, size)
        print(x, end="")
        return x

    def readline(self, size=None):
        line = io.StringIO.readline(self, size)
        print(line, end="")
        return line


class TimeoutError(Exception):
    pass


class Check:
    parts = None
    current_part = None
    part_counter = None

    @staticmethod
    def has_solution(part):
        return part["solution"].strip() != ""

    @staticmethod
    def initialize(parts):
        Check.parts = parts
        for part in Check.parts:
            part["valid"] = True
            part["feedback"] = []
            part["secret"] = []

    @staticmethod
    def part():
        if Check.part_counter is None:
            Check.part_counter = 0
        else:
            Check.part_counter += 1
        Check.current_part = Check.parts[Check.part_counter]
        return Check.has_solution(Check.current_part)

    @staticmethod
    def feedback(message, *args, **kwargs):
        Check.current_part["feedback"].append(message.format(*args, **kwargs))

    @staticmethod
    def error(message, *args, **kwargs):
        Check.current_part["valid"] = False
        Check.feedback(message, *args, **kwargs)

    @staticmethod
    def clean(x, digits=6, typed=False):
        t = type(x)
        if t is float:
            x = round(x, digits)
            # Since -0.0 differs from 0.0 even after rounding,
            # we change it to 0.0 abusing the fact it behaves as False.
            v = x if x else 0.0
        elif t is complex:
            v = complex(
                Check.clean(x.real, digits, typed), Check.clean(x.imag, digits, typed)
            )
        elif t is list:
            v = list([Check.clean(y, digits, typed) for y in x])
        elif t is tuple:
            v = tuple([Check.clean(y, digits, typed) for y in x])
        elif t is dict:
            v = sorted(
                [
                    (Check.clean(k, digits, typed), Check.clean(v, digits, typed))
                    for (k, v) in x.items()
                ]
            )
        elif t is set:
            v = sorted([Check.clean(y, digits, typed) for y in x])
        else:
            v = x
        return (t, v) if typed else v

    @staticmethod
    def secret(x, hint=None, clean=None):
        clean = Check.get("clean", clean)
        Check.current_part["secret"].append((str(clean(x)), hint))

    @staticmethod
    def equal(expression, expected_result, clean=None, env=None, update_env=None):
        global_env = Check.init_environment(env=env, update_env=update_env)
        clean = Check.get("clean", clean)
        actual_result = eval(expression, global_env)
        if clean(actual_result) != clean(expected_result):
            Check.error(
                "Izraz {0} vrne {1!r} namesto {2!r}.",
                expression,
                actual_result,
                expected_result,
            )
            return False
        else:
            return True

    @staticmethod
    def approx(expression, expected_result, tol=1e-6, env=None, update_env=None):
        try:
            import numpy as np
        except ImportError:
            Check.error("Namestiti morate numpy.")
            return False
        if not isinstance(expected_result, np.ndarray):
            Check.error("Ta funkcija je namenjena testiranju za tip np.ndarray.")

        if env is None:
            env = dict()
        env.update({"np": np})
        global_env = Check.init_environment(env=env, update_env=update_env)
        actual_result = eval(expression, global_env)
        if type(actual_result) is not type(expected_result):
            Check.error(
                "Rezultat ima napačen tip. Pričakovan tip: {}, dobljen tip: {}.",
                type(expected_result).__name__,
                type(actual_result).__name__,
            )
            return False
        exp_shape = expected_result.shape
        act_shape = actual_result.shape
        if exp_shape != act_shape:
            Check.error(
                "Obliki se ne ujemata. Pričakovana oblika: {}, dobljena oblika: {}.",
                exp_shape,
                act_shape,
            )
            return False
        try:
            np.testing.assert_allclose(
                expected_result, actual_result, atol=tol, rtol=tol
            )
            return True
        except AssertionError as e:
            Check.error("Rezultat ni pravilen." + str(e))
            return False

    @staticmethod
    def run(statements, expected_state, clean=None, env=None, update_env=None):
        code = "\n".join(statements)
        statements = "  >>> " + "\n  >>> ".join(statements)
        global_env = Check.init_environment(env=env, update_env=update_env)
        clean = Check.get("clean", clean)
        exec(code, global_env)
        errors = []
        for x, v in expected_state.items():
            if x not in global_env:
                errors.append(
                    "morajo nastaviti spremenljivko {0}, vendar je ne".format(x)
                )
            elif clean(global_env[x]) != clean(v):
                errors.append(
                    "nastavijo {0} na {1!r} namesto na {2!r}".format(
                        x, global_env[x], v
                    )
                )
        if errors:
            Check.error("Ukazi\n{0}\n{1}.", statements, ";\n".join(errors))
            return False
        else:
            return True

    @staticmethod
    @contextmanager
    def in_file(filename, content, encoding=None):
        encoding = Check.get("encoding", encoding)
        with open(filename, "w", encoding=encoding) as f:
            for line in content:
                print(line, file=f)
        old_feedback = Check.current_part["feedback"][:]
        yield
        new_feedback = Check.current_part["feedback"][len(old_feedback) :]
        Check.current_part["feedback"] = old_feedback
        if new_feedback:
            new_feedback = ["\n    ".join(error.split("\n")) for error in new_feedback]
            Check.error(
                "Pri vhodni datoteki {0} z vsebino\n  {1}\nso se pojavile naslednje napake:\n- {2}",
                filename,
                "\n  ".join(content),
                "\n- ".join(new_feedback),
            )

    @staticmethod
    @contextmanager
    def input(content, visible=None):
        old_stdin = sys.stdin
        old_feedback = Check.current_part["feedback"][:]
        try:
            with Check.set_stringio(visible):
                sys.stdin = Check.get("stringio")("\n".join(content) + "\n")
                yield
        finally:
            sys.stdin = old_stdin
        new_feedback = Check.current_part["feedback"][len(old_feedback) :]
        Check.current_part["feedback"] = old_feedback
        if new_feedback:
            new_feedback = ["\n  ".join(error.split("\n")) for error in new_feedback]
            Check.error(
                "Pri vhodu\n  {0}\nso se pojavile naslednje napake:\n- {1}",
                "\n  ".join(content),
                "\n- ".join(new_feedback),
            )

    @staticmethod
    def out_file(filename, content, encoding=None):
        encoding = Check.get("encoding", encoding)
        with open(filename, encoding=encoding) as f:
            out_lines = f.readlines()
        equal, diff, line_width = Check.difflines(out_lines, content)
        if equal:
            return True
        else:
            Check.error(
                "Izhodna datoteka {0}\n  je enaka{1}  namesto:\n  {2}",
                filename,
                (line_width - 7) * " ",
                "\n  ".join(diff),
            )
            return False

    @staticmethod
    def output(expression, content, env=None, update_env=None):
        global_env = Check.init_environment(env=env, update_env=update_env)
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        too_many_read_requests = False
        try:
            exec(expression, global_env)
        except EOFError:
            too_many_read_requests = True
        finally:
            output = sys.stdout.getvalue().rstrip().splitlines()
            sys.stdout = old_stdout
        equal, diff, line_width = Check.difflines(output, content)
        if equal and not too_many_read_requests:
            return True
        else:
            if too_many_read_requests:
                Check.error("Program prevečkrat zahteva uporabnikov vnos.")
            if not equal:
                Check.error(
                    "Program izpiše{0}  namesto:\n  {1}",
                    (line_width - 13) * " ",
                    "\n  ".join(diff),
                )
            return False

    @staticmethod
    def difflines(actual_lines, expected_lines):
        actual_len, expected_len = len(actual_lines), len(expected_lines)
        if actual_len < expected_len:
            actual_lines += (expected_len - actual_len) * ["\n"]
        else:
            expected_lines += (actual_len - expected_len) * ["\n"]
        equal = True
        line_width = max(
            len(actual_line.rstrip())
            for actual_line in actual_lines + ["Program izpiše"]
        )
        diff = []
        for out, given in zip(actual_lines, expected_lines):
            out, given = out.rstrip(), given.rstrip()
            if out != given:
                equal = False
            diff.append(
                "{0} {1} {2}".format(
                    out.ljust(line_width), "|" if out == given else "*", given
                )
            )
        return equal, diff, line_width

    @staticmethod
    def init_environment(env=None, update_env=None):
        global_env = globals()
        if not Check.get("update_env", update_env):
            global_env = dict(global_env)
        global_env.update(Check.get("env", env))
        return global_env

    @staticmethod
    def generator(
        expression,
        expected_values,
        should_stop=None,
        further_iter=None,
        clean=None,
        env=None,
        update_env=None,
    ):
        from types import GeneratorType

        global_env = Check.init_environment(env=env, update_env=update_env)
        clean = Check.get("clean", clean)
        gen = eval(expression, global_env)
        if not isinstance(gen, GeneratorType):
            Check.error("Izraz {0} ni generator.", expression)
            return False

        try:
            for iteration, expected_value in enumerate(expected_values):
                actual_value = next(gen)
                if clean(actual_value) != clean(expected_value):
                    Check.error(
                        "Vrednost #{0}, ki jo vrne generator {1} je {2!r} namesto {3!r}.",
                        iteration,
                        expression,
                        actual_value,
                        expected_value,
                    )
                    return False
            for _ in range(Check.get("further_iter", further_iter)):
                next(gen)  # we will not validate it
        except StopIteration:
            Check.error("Generator {0} se prehitro izteče.", expression)
            return False

        if Check.get("should_stop", should_stop):
            try:
                next(gen)
                Check.error("Generator {0} se ne izteče (dovolj zgodaj).", expression)
            except StopIteration:
                pass  # this is fine
        return True

    @staticmethod
    def summarize():
        for i, part in enumerate(Check.parts):
            if not Check.has_solution(part):
                print("{0}. podnaloga je brez rešitve.".format(i + 1))
            elif not part["valid"]:
                print("{0}. podnaloga nima veljavne rešitve.".format(i + 1))
            else:
                print("{0}. podnaloga ima veljavno rešitev.".format(i + 1))
            for message in part["feedback"]:
                print("  - {0}".format("\n    ".join(message.splitlines())))

    settings_stack = [
        {
            "clean": clean.__func__,
            "encoding": None,
            "env": {},
            "further_iter": 0,
            "should_stop": False,
            "stringio": VisibleStringIO,
            "update_env": False,
        }
    ]

    @staticmethod
    def get(key, value=None):
        if value is None:
            return Check.settings_stack[-1][key]
        return value

    @staticmethod
    @contextmanager
    def set(**kwargs):
        settings = dict(Check.settings_stack[-1])
        settings.update(kwargs)
        Check.settings_stack.append(settings)
        try:
            yield
        finally:
            Check.settings_stack.pop()

    @staticmethod
    @contextmanager
    def set_clean(clean=None, **kwargs):
        clean = clean or Check.clean
        with Check.set(clean=(lambda x: clean(x, **kwargs)) if kwargs else clean):
            yield

    @staticmethod
    @contextmanager
    def set_environment(**kwargs):
        env = dict(Check.get("env"))
        env.update(kwargs)
        with Check.set(env=env):
            yield

    @staticmethod
    @contextmanager
    def set_stringio(stringio):
        if stringio is True:
            stringio = VisibleStringIO
        elif stringio is False:
            stringio = io.StringIO
        if stringio is None or stringio is Check.get("stringio"):
            yield
        else:
            with Check.set(stringio=stringio):
                yield

    @staticmethod
    @contextmanager
    def time_limit(timeout_seconds=1):
        from signal import SIGINT, raise_signal
        from threading import Timer

        def interrupt_main():
            raise_signal(SIGINT)

        timer = Timer(timeout_seconds, interrupt_main)
        timer.start()
        try:
            yield
        except KeyboardInterrupt:
            raise TimeoutError
        finally:
            timer.cancel()


def _validate_current_file():
    def extract_parts(filename):
        with open(filename, encoding="utf-8") as f:
            source = f.read()
        part_regex = re.compile(
            r"# =+@(?P<part>\d+)=\s*\n"  # beginning of header
            r"(\s*#( [^\n]*)?\n)+?"  # description
            r"\s*# =+\s*?\n"  # end of header
            r"(?P<solution>.*?)"  # solution
            r"(?=\n\s*# =+@)",  # beginning of next part
            flags=re.DOTALL | re.MULTILINE,
        )
        parts = [
            {"part": int(match.group("part")), "solution": match.group("solution")}
            for match in part_regex.finditer(source)
        ]
        # The last solution extends all the way to the validation code,
        # so we strip any trailing whitespace from it.
        parts[-1]["solution"] = parts[-1]["solution"].rstrip()
        return parts

    def backup(filename):
        backup_filename = None
        suffix = 1
        while not backup_filename or os.path.exists(backup_filename):
            backup_filename = "{0}.{1}".format(filename, suffix)
            suffix += 1
        shutil.copy(filename, backup_filename)
        return backup_filename

    def submit_parts(parts, url, token):
        submitted_parts = []
        for part in parts:
            if Check.has_solution(part):
                submitted_part = {
                    "part": part["part"],
                    "solution": part["solution"],
                    "valid": part["valid"],
                    "secret": [x for (x, _) in part["secret"]],
                    "feedback": json.dumps(part["feedback"]),
                }
                if "token" in part:
                    submitted_part["token"] = part["token"]
                submitted_parts.append(submitted_part)
        data = json.dumps(submitted_parts).encode("utf-8")
        headers = {"Authorization": token, "content-type": "application/json"}
        request = urllib.request.Request(url, data=data, headers=headers)
        # This is a workaround because some clients (and not macOS ones!) report
        # <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1129)>
        import ssl

        context = ssl._create_unverified_context()
        response = urllib.request.urlopen(request, context=context)
        # When the issue is resolved, the following should be used
        # response = urllib.request.urlopen(request)
        return json.loads(response.read().decode("utf-8"))

    def update_attempts(old_parts, response):
        updates = {}
        for part in response["attempts"]:
            part["feedback"] = json.loads(part["feedback"])
            updates[part["part"]] = part
        for part in old_parts:
            valid_before = part["valid"]
            part.update(updates.get(part["part"], {}))
            valid_after = part["valid"]
            if valid_before and not valid_after:
                wrong_index = response["wrong_indices"].get(str(part["part"]))
                if wrong_index is not None:
                    hint = part["secret"][wrong_index][1]
                    if hint:
                        part["feedback"].append("Namig: {}".format(hint))

    filename = os.path.abspath(sys.argv[0])
    file_parts = extract_parts(filename)
    Check.initialize(file_parts)

    if Check.part():
        Check.current_part[
            "token"
        ] = "eyJwYXJ0IjoyNzM5NiwidXNlciI6NTg2M30:1rh8lr:xswWFOHLADe_cvovPvUkiUd3BX5WqYtwamZqg1x_QkE"
        try:
            primeri = [
                ("adventures_of_huckleberry_finn", 6871, 120867, [('and', 6439), ('what', 468), ('truth', 12), ('sun', 18), ('finn', 26), ('_was_', 28), ('hand', 77), ('doctor', 44), ('twenty', 21), ('myself', 69), ('soon', 101), ('again', 188)]),
                ("alice's_adventures_in_wonderland", 3044, 30537, [('the', 1818), ('and', 940), ('a', 690), ('she', 553), ('alice', 403), ('first', 51), ('rabbit', 51), ('child', 11), ('party', 11)]),
                ("dracula", 9787, 167231, [('the', 8090), ('dracula', 42), ('dead', 109), ('blood', 113), ('night', 319), ('neck', 32), ('storm', 18), ('teacher', 1), ('ghost', 3), ('sunrise', 26)]),
                ("frankenstein", 7353, 78606, [('the', 4371), ('elizabeth', 92), ('science', 28), ('stranger', 22), ('brother', 24), ('misery', 54), ('night', 91), ('danger', 12), ('frankenstein', 32), ('head', 25)]),
                ("grimms'_fairy_tales", 5181, 105336, [('the', 7224), ('castle', 82), ('mountain', 24), ('people', 45), ('show', 19), ('star', 8), ('smart', 5), ('promise', 10), ('eaten', 28), ('coin', 1)]),
                ("iliad", 13188, 199561, [('the', 15796), ('love', 81), ('walls', 113), ('eyes', 243), ('sky', 57), ('morning', 23), ('homer', 178), ('spartan', 35), ('achilles', 418), ('trojans', 118)]),
                ("metamorphosis", 3017, 25641, [('the', 1332), ('suddenly', 9), ('she', 200), ('thing', 11), ('like', 38), ('dish', 7), ('love', 2), ('probably', 15), ('perfect', 1), ('housekeeper', 1)]),
                ("moby_dick", 17647, 222663, [('the', 14703), ('and', 6517), ('green', 54), ('often', 73), ('starbuck', 199), ('human', 37), ('dick', 90), ('whale', 1230), ('whales', 271), ('fish', 169)]),
                ("peter_pan", 5340, 51746, [('the', 2546), ('peter', 409), ('pan', 32), ('yes', 55), ('mother', 102), ('night', 90), ('young', 7), ('money', 3), ('driver', 1), ('family', 4)]),
                ("war_and_peace", 17736, 576628, [('the', 34725), ('war', 302), ('peace', 115), ('life', 618), ('anna', 293), ('army', 665), ('fight', 77), ('snow', 65), ('destroy', 36), ('transport', 21)]),
            ]
            for naslov, velikost, vsota, rezultati in primeri:
                slovar = frekvence(naslov)
                if len(slovar) != velikost:
                    Check.error("Izraz len(frekvence(\"{}\")) vrne {} namesto {}.", naslov, len(slovar), velikost)
                    break
                if sum(slovar.values()) != vsota:
                    Check.error("Izraz sum(frekvence(\"{}\").values()) vrne {} namesto {}.", naslov, sum(slovar.values()), vsota)
                    break
                for beseda, frekvenca in rezultati:
                    rezultat = slovar[beseda]
                    if rezultat != frekvenca:
                        Check.error("Izraz frekvence(\"{}\")['{}'] vrne {} namesto {}.", naslov, beseda, rezultat, frekvenca)
                        break
                else: continue
                break
        except TimeoutError:
            Check.error("Dovoljen čas izvajanja presežen")
        except Exception:
            Check.error(
                "Testi sprožijo izjemo\n  {0}",
                "\n  ".join(traceback.format_exc().split("\n"))[:-2],
            )

    if Check.part():
        Check.current_part[
            "token"
        ] = "eyJwYXJ0IjoyNzM5OCwidXNlciI6NTg2M30:1rh8lr:tjE4X2cXDD5EMiuWljGb34yqjlhrFCbk7ZJhJ5qal7s"
        try:
            primeri = [
                ("adventures_of_huckleberry_finn", 6871, [('and', 1.0), ('what', 0.5363410467463892), ('truth', 0.5009318217114459), ('sun', 0.5013977325671688), ('finn', 0.5020189470414661), ('_was_', 0.5021742506600404), ('hand', 0.505979189315111), ('doctor', 0.5034166796086349), ('twenty', 0.5016306879950303), ('myself', 0.5053579748408138), ('soon', 0.5078428327380028), ('again', 0.5145985401459854)]),
                ("alice's_adventures_in_wonderland", 3044, [('the', 1.0), ('and', 0.7585258525852585), ('a', 0.6897689768976898), ('she', 0.6520902090209021), ('alice', 0.6108360836083608), ('first', 0.514026402640264), ('rabbit', 0.514026402640264), ('child', 0.503025302530253), ('party', 0.503025302530253)]),
                ("dracula", 9787, [('the', 1.0), ('dracula', 0.5025957972805933), ('dead', 0.5067367119901113), ('blood', 0.5069839307787392), ('night', 0.5197156983930779), ('neck', 0.5019777503090235), ('storm', 0.5011124845488257), ('teacher', 0.500061804697157), ('ghost', 0.500185414091471), ('sunrise', 0.5016069221260816)]),
                ("frankenstein", 7353, [('the', 1.0), ('elizabeth', 0.5105239075726379), ('science', 0.5032029283916724), ('stranger', 0.5025165865934569), ('brother', 0.502745367192862), ('misery', 0.5061770761839396), ('night', 0.5104095172729353), ('danger', 0.5013726835964311), ('frankenstein', 0.5036604895904827), ('head', 0.5028597574925646)]),
                ("grimms'_fairy_tales", 5181, [('the', 1.0), ('castle', 0.5056755260243633), ('mountain', 0.5016611295681063), ('people', 0.5031146179401993), ('show', 0.5013150609080842), ('star', 0.5005537098560354), ('smart', 0.5003460686600222), ('promise', 0.5006921373200443), ('eaten', 0.501937984496124), ('coin', 0.5000692137320044)]),
                ("iliad", 13188, [('the', 1.0), ('love', 0.502563940238035), ('walls', 0.5035768548999747), ('eyes', 0.5076918207141048), ('sky', 0.5018042542415801), ('morning', 0.5007280324132691), ('homer', 0.5056343378070397), ('spartan', 0.5011078754114966), ('achilles', 0.5132311977715878), ('trojans', 0.5037351228159027)]),
                ("metamorphosis", 3017, [('the', 1.0), ('suddenly', 0.5033783783783784), ('she', 0.575075075075075), ('thing', 0.5041291291291291), ('like', 0.5142642642642643), ('dish', 0.5026276276276276), ('love', 0.5007507507507507), ('probably', 0.5056306306306306), ('perfect', 0.5003753753753754), ('housekeeper', 0.5003753753753754)]),
                ("moby_dick", 17647, [('the', 1.0), ('and', 0.7216214378018091), ('green', 0.5018363599265456), ('often', 0.5024824865673672), ('starbuck', 0.5067673263959737), ('human', 0.5012582466163368), ('dick', 0.503060599877576), ('whale', 0.541828198326872), ('whales', 0.5092158062980344), ('fish', 0.5057471264367817)]),
                ("peter_pan", 5340, [('the', 1.0), ('peter', 0.5803220738413197), ('pan', 0.5062843676355067), ('yes', 0.5108012568735271), ('mother', 0.5200314218381775), ('night', 0.5176747839748626), ('young', 0.5013747054202671), ('money', 0.5005891594658287), ('driver', 0.5001963864886095), ('family', 0.5007855459544384)]),
                ("war_and_peace", 17736, [('the', 1.0), ('war', 0.5043484521238301), ('peace', 0.5016558675305975), ('life', 0.5088984881209503), ('anna', 0.5042188624910007), ('army', 0.5095752339812815), ('fight', 0.5011087113030958), ('snow', 0.50093592512599), ('destroy', 0.5005183585313175), ('transport', 0.5003023758099352)]),
            ]
            for naslov, velikost, rezultati in primeri:
                slovar = tf(frekvence(naslov))
                if len(slovar) != velikost:
                    Check.error("Izraz len(tf(frekvence(\"{}\"))) vrne {} namesto {}.", naslov, len(slovar), velikost)
                    break
                for beseda, stevilo in rezultati:
                    rezultat = slovar[beseda]
                    if rezultat != stevilo:
                        Check.error("Izraz tf(frekvence(\"{}\"))['{}'] vrne {} namesto {}.", naslov, beseda, rezultat, stevilo)
                        break
                else: continue
                break
        except TimeoutError:
            Check.error("Dovoljen čas izvajanja presežen")
        except Exception:
            Check.error(
                "Testi sprožijo izjemo\n  {0}",
                "\n  ".join(traceback.format_exc().split("\n"))[:-2],
            )

    if Check.part():
        Check.current_part[
            "token"
        ] = "eyJwYXJ0IjoyNzM5OSwidXNlciI6NTg2M30:1rh8lr:GfaxrIoEpDllVqa2RCoGnvZvwDk2ONUxKNkveSd8nFI"
        try:
            primeri = [
                ('the', 0.0), ('green', 0.10536051565782635), ('war', 0.22314355131420976), ('anna', 1.6094379124341003), ('castle', 0.5108256237659907), ('asopus', 2.302585092994046), ('expands', 2.302585092994046),
                ('merchantability', 2.302585092994046), ('screaming', 0.10536051565782635), ('four', 0.0), ('woods', 0.22314355131420976), ('sky', 0.0), ('dracula', 2.302585092994046), ('night', 0.0),
                ('danger', 0.10536051565782635), ('blood', 0.22314355131420976), ('child', 0.0), ('fish', 0.10536051565782635), ('castle', 0.5108256237659907), ('army', 0.3566749439387324), ('finn', 2.302585092994046),
                ('whale', 0.9162907318741551), ('snow', 0.22314355131420976)
            ]
            naslovi = [
                "adventures_of_huckleberry_finn", "alice's_adventures_in_wonderland", "dracula",
                "frankenstein", "grimms'_fairy_tales", "iliad", "metamorphosis", "moby_dick",
                "peter_pan", "war_and_peace"
            ]
            docs = {naslov: frekvence(naslov) for naslov in naslovi}
            slovar = idf(docs)
            for beseda, stevilo in primeri:
                rezultat = slovar[beseda]
                if rezultat != stevilo:
                    Check.error("Izraz idf(docs)['{}'] vrne {} namesto {}.", beseda, rezultat, stevilo)
                    break
        except TimeoutError:
            Check.error("Dovoljen čas izvajanja presežen")
        except Exception:
            Check.error(
                "Testi sprožijo izjemo\n  {0}",
                "\n  ".join(traceback.format_exc().split("\n"))[:-2],
            )

    if Check.part():
        Check.current_part[
            "token"
        ] = "eyJwYXJ0IjoyNzQwMCwidXNlciI6NTg2M30:1rh8lr:E7teRjg4kpNPTtYB8HFPe9wgXdA8tFIiJEj45ENgI98"
        try:
            primeri = [
                ("adventures_of_huckleberry_finn", 6871, [('and', 0.0), ('what', 0.0), ('truth', 0.05277843504493227), ('sun', 0.05282752365294182), ('finn', 1.1559413438582473), ('_was_', 0.8082182776604541), ('hand', 0.0), ('doctor', 0.17955611597723267), ('twenty', 0.052852067956946594), ('myself', 0.05324477682102298), ('soon', 0.0), ('again', 0.0)]),
                ("alice's_adventures_in_wonderland", 3044, [('the', 0.0), ('and', 0.0), ('a', 0.0), ('she', 0.0), ('alice', 1.4065020603794762), ('first', 0.0), ('rabbit', 0.47099762867788664), ('child', 0.0), ('party', 0.0)]),
                ("dracula", 9787, [('the', 0.0), ('dracula', 1.1572695906197517), ('dead', 0.0), ('blood', 0.11313019477320535), ('night', 0.0), ('neck', 0.0), ('storm', 0.17873426733345132), ('teacher', 0.3466164300315524), ('ghost', 0.255507526151926), ('sunrise', 0.3476874238210455)]),
                ("frankenstein", 7353, [('the', 0.0), ('elizabeth', 0.8216565320514059), ('science', 0.17947987627390571), ('stranger', 0.05294540669009736), ('brother', 0.0), ('misery', 0.18054068027097814), ('night', 0.0), ('danger', 0.05282488448046819), ('frankenstein', 1.1597211352611283), ('head', 0.0)]),
                ("grimms'_fairy_tales", 5181, [('the', 0.0), ('castle', 0.25831201600459086), ('mountain', 0.2562613594307794), ('people', 0.0), ('show', 0.0), ('star', 0.11169533244077831), ('smart', 0.17846090598927855), ('promise', 0.0), ('eaten', 0.17902870248087538), ('coin', 0.4582087858382316)]),
                ("iliad", 13188, [('the', 0.0), ('love', 0.0), ('walls', 0.05305711710560773), ('eyes', 0.0), ('sky', 0.0), ('morning', 0.0), ('homer', 0.8137870730951606), ('spartan', 1.1538435239044296), ('achilles', 0.6179164044486176), ('trojans', 1.1598929846134225)]),
                ("metamorphosis", 3017, [('the', 0.0), ('suddenly', 0.05303620551694638), ('she', 0.0), ('thing', 0.0), ('like', 0.0), ('dish', 0.17927468090614213), ('love', 0.0), ('probably', 0.18034577683388608), ('perfect', 0.052719807572027974), ('housekeeper', 0.6024383439063337)]),
                ("moby_dick", 17647, [('the', 0.0), ('and', 0.0), ('green', 0.05287373765770739), ('often', 0.0), ('starbuck', 1.1668748913758171), ('human', 0.05281282734123513), ('dick', 0.8096448016948121), ('whale', 0.49647215639498443), ('whales', 0.8195512242667558), ('fish', 0.05328577803384322)]),
                ("peter_pan", 5340, [('the', 0.0), ('peter', 0.40224860929981116), ('pan', 0.25862302790037783), ('yes', 0.0), ('mother', 0.054790778763143005), ('night', 0.0), ('young', 0.0), ('money', 0.0), ('driver', 0.2555131311335385), ('family', 0.0)]),
                ("war_and_peace", 17736, [('the', 0.0), ('war', 0.11254210470673615), ('peace', 0.052854720885797984), ('life', 0.0), ('anna', 0.8115089534574128), ('army', 0.18175271801284001), ('fight', 0.052797072223523006), ('snow', 0.11178062131348247), ('destroy', 0.0), ('transport', 0.4584224300892641)]),
            ]
            for naslov, velikost, rezultati in primeri:
                slovar = tfidf(naslov, docs)
                if len(slovar) != velikost:
                    Check.error("Izraz len(tfidf(\"{}\", docs)) vrne {} namesto {}.", naslov, len(slovar), velikost)
                    break
                for beseda, stevilo in rezultati:
                    rezultat = slovar[beseda]
                    if rezultat != stevilo:
                        Check.error("Izraz tfidf(\"{}\", docs)['{}'] vrne {} namesto {}.", naslov, beseda, rezultat, stevilo)
                        break
                else: continue
                break
        except TimeoutError:
            Check.error("Dovoljen čas izvajanja presežen")
        except Exception:
            Check.error(
                "Testi sprožijo izjemo\n  {0}",
                "\n  ".join(traceback.format_exc().split("\n"))[:-2],
            )

    if Check.part():
        Check.current_part[
            "token"
        ] = "eyJwYXJ0IjoyNzQwMSwidXNlciI6NTg2M30:1rh8lr:xr2kCRBaqIoc4eLk3rbGQ3OTQvfiKP8yj2KP_ncVBpo"
        try:
            primeri = [
                ("adventures_of_huckleberry_finn", 10, [" Novel | 'adventures_of_huckleberry_finn'", "1.2200 | 'jim'", "1.1804 | 'nigger'", "1.1679 | 'knowed'", "1.1676 | 'huck'", "1.1608 | 'sawyer'", "1.1597 | 'niggers'", "1.1595 | 'gwyne'", "1.1584 | 'ben'", "1.1574 | 'doan'", "1.1568 | 'wuz'"]),
                ("alice's_adventures_in_wonderland", 10, [" Novel | 'alice's_adventures_in_wonderland'", "1.4065 | 'alice'", "1.1868 | 'hatter'", "1.1861 | 'gryphon'", "1.1779 | 'duchess'", "1.1766 | 'dormouse'", "1.1602 | 'dinah'", "1.1595 | 'dodo'", "1.1570 | 'croquet'", "1.1564 | 'gardeners'", "1.1564 | 'twinkle'"]),
                ("dracula", 10, [" Novel | 'dracula'", "1.1973 | 'helsing'", "1.1936 | 'lucy'", "1.1837 | 'mina'", "1.1762 | 'harker'", "1.1711 | 'seward'", "1.1640 | 'godalming'", "1.1634 | 'quincey'", "1.1624 | 'morris'", "1.1581 | 'renfield'", "1.1577 | 'westenra'"]),
                ("frankenstein", 10, [" Novel | 'frankenstein'", "1.1668 | 'clerval'", "1.1658 | 'justine'", "1.1597 | 'frankenstein'", "1.1579 | 'safie'", "1.1574 | 'cottagers'", "1.1560 | 'dæmon'", "1.1555 | 'ingolstadt'", "1.1550 | 'hovel'", "1.1547 | 'ernest'", "1.1547 | 'kirwin'"]),
                ("grimms'_fairy_tales", 10, [" Novel | 'grimms'_fairy_tales'", "1.1669 | 'gretel'", "1.1623 | 'tailor'", "1.1612 | 'dwarf'", "1.1588 | 'hansel'", "1.1570 | 'snowdrop'", "1.1569 | 'chanticleer'", "1.1558 | 'goodbye'", "1.1554 | 'rapunzel'", "1.1548 | 'dummling'", "1.1548 | 'partlet'"]),
                ("iliad", 10, [" Novel | 'iliad'", "1.1847 | 'hector'", "1.1772 | 'troy'", "1.1679 | 'trojan'", "1.1632 | 'ajax'", "1.1632 | 'patroclus'", "1.1603 | 'ulysses'", "1.1599 | 'trojans'", "1.1586 | 'coursers'", "1.1584 | 'nestor'", "1.1584 | 'priam'"]),
                ("metamorphosis", 10, [" Novel | 'metamorphosis'", "1.4089 | 'gregor'", "1.1807 | 'samsa'", "1.1591 | 'charwoman'", "1.1565 | 'metamorphosis'", "1.1556 | 'alright'", "1.1556 | 'wyllie'", "1.1547 | '5200'", "1.1547 | 'kafka'", "1.1547 | 'nonetheless'", "1.1539 | 'hallway'"]),
                ("moby_dick", 10, [" Novel | 'moby_dick'", "1.1914 | 'ahab'", "1.1716 | 'stubb'", "1.1711 | 'queequeg'", "1.1669 | 'starbuck'", "1.1652 | 'pequod'", "1.1616 | 'whaling'", "1.1587 | 'leviathan'", "1.1587 | 'nantucket'", "1.1583 | 'moby'", "1.1576 | 'harpooneer'"]),
                ("peter_pan", 10, [" Novel | 'peter_pan'", "1.3150 | 'wendy'", "1.1802 | 'nana'", "1.1762 | 'smee'", "1.1716 | 'tootles'", "1.1685 | 'nibs'", "1.1662 | 'lagoon'", "1.1644 | 'starkey'", "1.1630 | 'redskins'", "1.1612 | 'neverland'", "1.1567 | 'cecco'"]),
                ("war_and_peace", 10, [" Novel | 'war_and_peace'", "1.2164 | 'pierre'", "1.1915 | 'natásha'", "1.1770 | 'rostóv'", "1.1752 | 'moscow'", "1.1688 | 'kutúzov'", "1.1675 | 'countess'", "1.1661 | 'sónya'", "1.1656 | 'denísov'", "1.1622 | 'dólokhov'", "1.1610 | 'borís'"]),
            ]
            for naslov, n, vrstice in primeri:
                old_stdout = sys.stdout
                sys.stdout = io.StringIO()
                try:
                    karakteristicne_besede(naslov, docs, n)
                finally:
                    output = sys.stdout.getvalue().rstrip().splitlines()
                    sys.stdout = old_stdout
                equal, diff, line_width = Check.difflines(output, vrstice)
                if not equal:
                    Check.error('Program izpiše{0}  namesto:\n  {1}', (line_width - 13) * ' ', '\n  '.join(diff))
                    break
        except TimeoutError:
            Check.error("Dovoljen čas izvajanja presežen")
        except Exception:
            Check.error(
                "Testi sprožijo izjemo\n  {0}",
                "\n  ".join(traceback.format_exc().split("\n"))[:-2],
            )

    print("Shranjujem rešitve na strežnik... ", end="")
    try:
        url = "https://www.projekt-tomo.si/api/attempts/submit/"
        token = "Token fcbcc27df50a3648ded3309bbbab4d59b487bbb3"
        response = submit_parts(Check.parts, url, token)
    except urllib.error.URLError:
        message = (
            "\n"
            "-------------------------------------------------------------------\n"
            "PRI SHRANJEVANJU JE PRIŠLO DO NAPAKE!\n"
            "Preberite napako in poskusite znova ali se posvetujte z asistentom.\n"
            "-------------------------------------------------------------------\n"
        )
        print(message)
        traceback.print_exc()
        print(message)
        sys.exit(1)
    else:
        print("Rešitve so shranjene.")
        update_attempts(Check.parts, response)
        if "update" in response:
            print("Updating file... ", end="")
            backup_filename = backup(filename)
            with open(__file__, "w", encoding="utf-8") as f:
                f.write(response["update"])
            print("Previous file has been renamed to {0}.".format(backup_filename))
            print("If the file did not refresh in your editor, close and reopen it.")
    Check.summarize()


if __name__ == "__main__":
    _validate_current_file()
