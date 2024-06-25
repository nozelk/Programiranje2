# =============================================================================
# Meritve po krajih
# =====================================================================@040111=
# 1. podnaloga
# Podana je datoteka, ki vsebuje podatke o rezultatih meritev v različnih krajih,
# pri čemer so meritve v posameznem kraju izvedene ob različnih dnevih. Datoteka
# v vsaki vrstici vsebuje datum, ime kraja in rezultat meritve, ločeno z vejicami.
# Pri tem je datum zapisan kot niz oblike `yyyy-mm-dd`. Primer takšne datoteke bi bil
# 
#     2018-01-01,Murska Sobota,24.13
#     2018-01-02,Maribor,29.97
#     2018-01-04,Celje,25.27
#     2018-01-04,Murska Sobota,27.45
#     2018-01-07,Celje,25.31
#     2018-01-07,Kranj,22.06
#     2018-01-07,Maribor,23.01
#     2018-01-08,Ljubljana,27.22
#     2018-01-08,Maribor,26.29
#     2018-01-10,Koper,20.97
#     2018-01-10,Kranj,21.15
#     2018-01-11,Celje,24.86
#     2018-01-11,Koper,22.56
#     2018-01-14,Maribor,29.06
#     ...
# 
# Sestavite funkcijo `meritve(vhod, izhod, zacetek, konec)`, ki za parametre prejme
# ime vhodne datoteke, ime izhodne datoteke ter začetek in konec časovnega obdobja
# (dva datuma v enaki obliki kot je prikazano zgoraj). Funkcija naj prebere vsebino
# vhodne datoteke in za vsak kraj izračuna povprečno izmerjeno vrednost v danem
# časovnem obdobju. Povprečno vrednost izračunate tako, da vsoto vseh izmerjenih
# vrednosti delite s številom meritev.
# 
# Funkcija naj končni rezultat zapiše v izhodno datoteko, ki naj za vsak kraj vsebuje
# ime kraja in povprečno izmerjeno vrednost izpisano na dve decimalni mesti, ločeno
# z vejico. Vrstice uredite naraščajoče glede na ime kraja. Primer:
# 
#     Celje,24.29
#     Koper,27.01
#     Kranj,24.82
#     Ljubljana,26.98
#     Maribor,26.12
#     Murska Sobota,25.98
#     Novo mesto,25.18
# =============================================================================

def meritve(vhod, izhod, zacetek, konec):
    with open(vhod, "r", encoding="utf-8") as dat:
        vrstice = dat.readlines()
        slo = {}
        for vrstica in vrstice:
            datum, mesto, temp = vrstica.split(",") 
            if zacetek <= datum <= konec:
                if mesto not in slo:
                    slo[mesto] = [float(temp), 1]
                else:
                    slo[mesto][0] += float(temp)
                    slo[mesto][1] += 1
            elif konec <= datum:
                break
    for m, p in slo.items():
        slo[m] = float("{:.2f}".format(p[0] / p[1]))
    slo = dict(sorted(slo.items(), key=lambda item: item[0]))
    with open(izhod, "w", encoding="utf-8") as dato:
        for m, v in slo.items():
            dato.write(f"{m},{float(v):.2f}\n")
    return izhod



































































































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
        ] = "eyJwYXJ0Ijo0MDExMSwidXNlciI6NTg2M30:1rmdIi:IifwTFKwxmeNfDqROFrdFevu-1OWvwTT5ApcdHxZdXo"
        try:
            podatki = [
                '2018-01-01,Murska Sobota,24.13',
                '2018-01-02,Maribor,29.97',
                '2018-01-04,Celje,25.27',
                '2018-01-04,Murska Sobota,27.45',
                '2018-01-07,Celje,25.31',
                '2018-01-07,Kranj,22.06',
                '2018-01-07,Maribor,23.01',
                '2018-01-08,Ljubljana,27.22',
                '2018-01-08,Maribor,26.29',
                '2018-01-10,Koper,20.97',
                '2018-01-10,Kranj,21.15',
                '2018-01-11,Celje,24.86',
                '2018-01-11,Koper,22.56',
                '2018-01-14,Maribor,29.06',
                '2018-01-14,Novo mesto,20.16',
                '2018-01-16,Celje,25.78',
                '2018-01-16,Ljubljana,26.65',
                '2018-01-16,Novo mesto,25.09',
                '2018-01-17,Celje,28.07',
                '2018-01-17,Kranj,24.32',
                '2018-01-17,Murska Sobota,26.22',
                '2018-01-18,Ljubljana,23.45',
                '2018-01-18,Maribor,27.97',
                '2018-01-18,Novo mesto,26.95',
                '2018-01-19,Ljubljana,24.35',
                '2018-01-19,Maribor,25.06',
                '2018-01-19,Murska Sobota,22.0',
                '2018-01-19,Novo mesto,27.01',
                '2018-01-20,Celje,20.0',
                '2018-01-21,Kranj,23.06',
                '2018-01-23,Maribor,21.38',
                '2018-01-24,Maribor,27.73',
                '2018-01-24,Novo mesto,20.93',
                '2018-01-25,Celje,20.57',
                '2018-01-27,Koper,22.46',
                '2018-01-29,Murska Sobota,27.54',
                '2018-01-30,Kranj,27.05',
                '2018-01-31,Kranj,28.08',
                '2018-01-31,Ljubljana,27.43',
                '2018-02-02,Maribor,22.81',
                '2018-02-02,Murska Sobota,22.88',
                '2018-02-03,Ljubljana,24.95',
                '2018-02-03,Maribor,20.19',
                '2018-02-03,Murska Sobota,24.13',
                '2018-02-04,Maribor,27.06',
                '2018-02-06,Maribor,29.97',
                '2018-02-07,Maribor,25.88',
                '2018-02-08,Maribor,20.75',
                '2018-02-09,Kranj,22.77',
                '2018-02-09,Murska Sobota,24.44',
                '2018-02-10,Ljubljana,28.45',
                '2018-02-10,Maribor,24.37',
                '2018-02-13,Celje,28.83',
                '2018-02-13,Koper,24.78',
                '2018-02-13,Ptuj,25',
                '2018-02-14,Celje,25.13',
                '2018-02-15,Ljubljana,26.04',
                '2018-02-15,Maribor,28.77',
                '2018-02-16,Celje,27.55',
                '2018-02-16,Ljubljana,22.76',
                '2018-02-16,Maribor,29.69',
                '2018-02-17,Celje,26.4',
                '2018-02-17,Koper,25.6',
                '2018-02-18,Kranj,23.34',
                '2018-02-19,Kranj,20.51',
                '2018-02-20,Koper,24.17',
                '2018-02-20,Kranj,26.09',
                '2018-02-21,Celje,26.18',
                '2018-02-22,Ljubljana,27.69',
                '2018-02-26,Celje,28.63',
                '2018-02-26,Koper,20.83',
                '2018-02-26,Murska Sobota,29.64',
                '2018-02-28,Maribor,28.97',
                '2018-03-03,Kranj,28.03',
                '2018-03-03,Maribor,29.29',
                '2018-03-03,Murska Sobota,22.54',
                '2018-03-06,Celje,26.96',
                '2018-03-07,Celje,24.7',
                '2018-03-07,Koper,22.3',
                '2018-03-08,Celje,24.52',
                '2018-03-08,Ljubljana,23.54',
                '2018-03-09,Celje,24.59',
                '2018-03-09,Ljubljana,28.53',
                '2018-03-10,Koper,24.67',
                '2018-03-12,Koper,25.69',
                '2018-03-12,Kranj,25.86',
                '2018-03-13,Maribor,29.49',
                '2018-03-13,Novo mesto,24.12',
                '2018-03-15,Murska Sobota,25.85',
                '2018-03-16,Koper,27.21',
                '2018-03-16,Maribor,24.29',
                '2018-03-16,Murska Sobota,25.25',
                '2018-03-18,Kranj,22.88',
                '2018-03-18,Murska Sobota,27.33',
                '2018-03-19,Ljubljana,24.7',
                '2018-03-19,Murska Sobota,27.08',
                '2018-03-21,Kranj,29.83',
                '2018-03-21,Ljubljana,28.83',
                '2018-03-21,Murska Sobota,20.76',
                '2018-03-22,Novo mesto,22.84',
                '2018-03-23,Koper,22.83',
                '2018-03-24,Celje,22.59',
                '2018-03-25,Maribor,26.14',
                '2018-03-26,Novo mesto,24.13',
                '2018-03-27,Koper,25.99',
                '2018-03-28,Novo mesto,21.34',
                '2018-03-29,Kranj,25.08',
                '2018-03-31,Murska Sobota,29.91',
                '2018-04-02,Koper,26.76',
                '2018-04-03,Koper,26.96',
                '2018-04-03,Murska Sobota,28.99',
                '2018-04-04,Celje,21.66',
                '2018-04-05,Novo mesto,25.02',
                '2018-04-06,Kranj,20.18',
                '2018-04-06,Ljubljana,27.55',
                '2018-04-07,Maribor,22.74',
                '2018-04-07,Murska Sobota,24.62',
                '2018-04-08,Celje,27.21',
                '2018-04-09,Celje,28.27',
                '2018-04-09,Kranj,27.53',
                '2018-04-10,Celje,28.43',
                '2018-04-10,Kranj,26.65',
                '2018-04-11,Maribor,28.02',
                '2018-04-12,Ljubljana,22.02',
                '2018-04-13,Maribor,26.87',
                '2018-04-15,Murska Sobota,24.84',
                '2018-04-16,Maribor,20.8',
                '2018-04-18,Koper,20.85',
                '2018-04-18,Maribor,24.09',
                '2018-04-19,Maribor,21.92',
                '2018-04-20,Maribor,21.43',
                '2018-04-20,Murska Sobota,23.21',
                '2018-04-21,Kranj,27.8',
                '2018-04-21,Maribor,25.5',
                '2018-04-21,Murska Sobota,20.52',
                '2018-04-22,Kranj,27.26',
                '2018-04-22,Ljubljana,25.11',
                '2018-04-23,Koper,20.74',
                '2018-04-25,Celje,21.71',
                '2018-04-26,Kranj,29.74',
                '2018-04-28,Kranj,28.38',
                '2018-04-28,Murska Sobota,29.42',
                '2018-04-28,Novo mesto,24.21',
                '2018-04-29,Celje,22.86',
                '2018-04-29,Murska Sobota,27.02',
                '2018-04-30,Koper,27.98',
                '2018-05-04,Ljubljana,22.97',
                '2018-05-04,Novo mesto,23.01',
                '2018-05-05,Celje,26.19',
                '2018-05-05,Ljubljana,24.09',
                '2018-05-06,Koper,25.98',
                '2018-05-06,Murska Sobota,29.72',
                '2018-05-07,Koper,20.11',
                '2018-05-07,Ljubljana,29.06',
                '2018-05-07,Maribor,27.92',
                '2018-05-08,Ljubljana,27.0',
                '2018-05-08,Murska Sobota,21.82',
                '2018-05-09,Maribor,25.21',
                '2018-05-09,Novo mesto,28.39',
                '2018-05-10,Koper,22.59',
                '2018-05-10,Maribor,23.13',
                '2018-05-11,Ljubljana,21.62',
                '2018-05-11,Maribor,24.45',
                '2018-05-11,Murska Sobota,28.13',
                '2018-05-12,Novo mesto,21.75',
                '2018-05-13,Kranj,25.36',
                '2018-05-15,Ljubljana,25.07',
                '2018-05-16,Kranj,22.39',
                '2018-05-17,Maribor,20.69',
                '2018-05-17,Novo mesto,28.62',
                '2018-05-18,Maribor,20.9',
                '2018-05-19,Ljubljana,28.47',
                '2018-05-20,Maribor,29.85',
                '2018-05-20,Murska Sobota,29.82',
                '2018-05-20,Novo mesto,25.66',
                '2018-05-21,Celje,29.75',
                '2018-05-21,Maribor,22.81',
                '2018-05-22,Kranj,27.27',
                '2018-05-22,Ljubljana,21.82',
                '2018-05-22,Maribor,26.3',
                '2018-05-23,Koper,29.26',
                '2018-05-23,Maribor,27.99',
                '2018-05-24,Koper,25.19',
                '2018-05-26,Celje,25.99',
                '2018-05-26,Maribor,25.48',
                '2018-05-26,Novo mesto,26.44',
                '2018-05-27,Murska Sobota,26.4',
                '2018-05-28,Ljubljana,22.66',
                '2018-05-29,Maribor,29.56',
                '2018-05-30,Maribor,22.47',
                '2018-05-31,Kranj,25.99',
                '2018-05-31,Murska Sobota,22.1',
                '2018-06-02,Ljubljana,24.1',
                '2018-06-02,Murska Sobota,23.91',
                '2018-06-05,Celje,26.88',
                '2018-06-05,Koper,24.12',
                '2018-06-06,Koper,21.87',
                '2018-06-07,Koper,20.09',
                '2018-06-07,Kranj,29.52',
                '2018-06-08,Novo mesto,29.6',
                '2018-06-11,Murska Sobota,24.11',
                '2018-06-13,Kranj,28.76',
                '2018-06-13,Ljubljana,28.71',
                '2018-06-13,Maribor,28.76',
                '2018-06-13,Novo mesto,20.68',
                '2018-06-14,Koper,26.28',
                '2018-06-14,Maribor,23.67',
                '2018-06-14,Novo mesto,21.49',
                '2018-06-15,Celje,21.15',
                '2018-06-16,Kranj,26.99',
                '2018-06-17,Murska Sobota,29.48',
                '2018-06-18,Maribor,22.23',
                '2018-06-18,Novo mesto,28.77',
                '2018-06-19,Murska Sobota,20.77',
                '2018-06-22,Murska Sobota,21.89',
                '2018-06-23,Kranj,25.88',
                '2018-06-23,Novo mesto,27.65',
                '2018-06-24,Ljubljana,29.29',
                '2018-06-24,Murska Sobota,21.11',
                '2018-06-25,Celje,29.79',
                '2018-06-26,Kranj,28.48',
                '2018-06-26,Ljubljana,29.54',
                '2018-06-26,Novo mesto,22.04',
                '2018-06-27,Ljubljana,28.65',
                '2018-06-27,Novo mesto,25.26',
                '2018-06-28,Novo mesto,23.03',
                '2018-06-30,Koper,25.86',
                '2018-06-30,Ljubljana,20.23',
                '2018-06-30,Murska Sobota,26.75',
                '2018-07-02,Murska Sobota,29.46',
                '2018-07-04,Koper,25.58',
                '2018-07-04,Kranj,23.2',
                '2018-07-07,Celje,27.46',
                '2018-07-07,Ljubljana,28.27',
                '2018-07-07,Maribor,25.36',
                '2018-07-08,Koper,29.03',
                '2018-07-08,Maribor,20.91',
                '2018-07-09,Koper,24.64',
                '2018-07-09,Kranj,21.02',
                '2018-07-09,Murska Sobota,29.65',
                '2018-07-11,Ljubljana,23.84',
                '2018-07-12,Celje,26.3',
                '2018-07-14,Kranj,25.19',
                '2018-07-14,Murska Sobota,20.78',
                '2018-07-15,Ljubljana,23.64',
                '2018-07-15,Novo mesto,21.04',
                '2018-07-16,Maribor,21.36',
                '2018-07-16,Murska Sobota,28.82',
                '2018-07-18,Celje,27.08',
                '2018-07-20,Celje,25.01',
                '2018-07-20,Murska Sobota,20.17',
                '2018-07-21,Koper,22.63',
                '2018-07-22,Koper,26.83',
                '2018-07-22,Novo mesto,23.77',
                '2018-07-23,Novo mesto,21.96',
                '2018-07-25,Koper,23.96',
                '2018-07-25,Maribor,27.93',
                '2018-07-26,Novo mesto,24.4',
                '2018-07-28,Celje,22.13',
                '2018-07-28,Kranj,25.1',
                '2018-07-30,Murska Sobota,27.75',
                '2018-07-30,Novo mesto,26.49',
                '2018-07-31,Celje,24.89',
                '2018-07-31,Kranj,27.95',
                '2018-07-31,Maribor,25.86',
                '2018-07-31,Novo mesto,28.25',
                '2018-08-01,Koper,22.32',
                '2018-08-03,Kranj,23.33',
                '2018-08-03,Ljubljana,23.32',
                '2018-08-04,Celje,27.95',
                '2018-08-04,Koper,25.89',
                '2018-08-06,Ljubljana,23.14',
                '2018-08-06,Maribor,29.2',
                '2018-08-07,Celje,26.23',
                '2018-08-09,Maribor,25.52',
                '2018-08-10,Celje,25.65',
                '2018-08-12,Celje,26.41',
                '2018-08-12,Maribor,24.43',
                '2018-08-12,Novo mesto,25.22',
                '2018-08-13,Celje,24.42',
                '2018-08-13,Maribor,28.21',
                '2018-08-13,Novo mesto,28.93',
                '2018-08-14,Celje,25.05',
                '2018-08-15,Ljubljana,23.52',
                '2018-08-15,Murska Sobota,29.38',
                '2018-08-18,Koper,21.15',
                '2018-08-19,Celje,24.33',
                '2018-08-21,Celje,26.06',
                '2018-08-21,Kranj,20.07',
                '2018-08-22,Celje,25.32',
                '2018-08-22,Kranj,21.89',
                '2018-08-23,Ljubljana,28.19',
                '2018-08-24,Celje,29.45',
                '2018-08-24,Novo mesto,20.03',
                '2018-08-25,Celje,21.04',
                '2018-08-25,Ljubljana,24.61',
                '2018-08-26,Novo mesto,20.77',
                '2018-08-29,Kranj,26.05',
                '2018-08-31,Kranj,21.97',
                '2018-08-31,Maribor,22.11',
                '2018-09-01,Maribor,26.91',
                '2018-09-01,Murska Sobota,25.33',
                '2018-09-02,Kranj,26.81',
                '2018-09-02,Murska Sobota,29.97',
                '2018-09-03,Kranj,26.98',
                '2018-09-04,Kranj,29.36',
                '2018-09-04,Murska Sobota,24.18',
                '2018-09-05,Murska Sobota,28.23',
                '2018-09-08,Murska Sobota,27.95',
                '2018-09-10,Ljubljana,23.52',
                '2018-09-11,Maribor,28.33',
                '2018-09-12,Kranj,25.36',
                '2018-09-13,Ljubljana,24.23',
                '2018-09-13,Maribor,23.41',
                '2018-09-15,Maribor,28.52',
                '2018-09-16,Kranj,22.65',
                '2018-09-16,Murska Sobota,23.59',
                '2018-09-17,Murska Sobota,26.77',
                '2018-09-20,Novo mesto,25.55',
                '2018-09-21,Celje,26.13',
                '2018-09-21,Kranj,28.43',
                '2018-09-23,Maribor,20.5',
                '2018-09-24,Kranj,28.91',
                '2018-09-25,Kranj,24.53',
                '2018-09-25,Maribor,23.24',
                '2018-09-25,Murska Sobota,23.98',
                '2018-09-26,Murska Sobota,28.88',
                '2018-09-27,Maribor,23.22',
                '2018-09-27,Murska Sobota,24.46',
                '2018-09-28,Celje,29.25',
                '2018-09-30,Kranj,23.86',
                '2018-10-03,Koper,25.08',
                '2018-10-04,Murska Sobota,23.12',
                '2018-10-06,Murska Sobota,27.16',
                '2018-10-07,Novo mesto,21.63',
                '2018-10-08,Celje,24.39',
                '2018-10-08,Koper,25.69',
                '2018-10-09,Celje,29.28',
                '2018-10-09,Maribor,22.17',
                '2018-10-09,Murska Sobota,22.27',
                '2018-10-10,Murska Sobota,21.62',
                '2018-10-11,Ljubljana,23.28',
                '2018-10-12,Celje,29.42',
                '2018-10-12,Ljubljana,24.19',
                '2018-10-12,Maribor,20.69',
                '2018-10-13,Murska Sobota,22.51',
                '2018-10-14,Celje,21.94',
                '2018-10-14,Koper,23.37',
                '2018-10-15,Koper,24.5',
                '2018-10-16,Kranj,29.51',
                '2018-10-16,Ljubljana,25.83',
                '2018-10-16,Maribor,23.34',
                '2018-10-17,Celje,28.12',
                '2018-10-17,Ljubljana,25.64',
                '2018-10-17,Murska Sobota,25.82',
                '2018-10-18,Koper,27.57',
                '2018-10-19,Koper,22.06',
                '2018-10-20,Ljubljana,29.36',
                '2018-10-23,Murska Sobota,27.65',
                '2018-10-24,Koper,25.7',
                '2018-10-24,Maribor,27.62',
                '2018-10-24,Novo mesto,26.57',
                '2018-10-25,Novo mesto,27.93',
                '2018-10-27,Kranj,20.25',
                '2018-10-27,Murska Sobota,20.86',
                '2018-10-29,Celje,21.93',
                '2018-10-30,Murska Sobota,29.36',
                '2018-10-31,Maribor,21.16',
                '2018-10-31,Murska Sobota,23.08',
                '2018-11-01,Koper,23.96',
                '2018-11-01,Murska Sobota,26.48',
                '2018-11-02,Koper,28.0',
                '2018-11-02,Murska Sobota,29.4',
                '2018-11-03,Celje,22.64',
                '2018-11-03,Ljubljana,21.14',
                '2018-11-03,Novo mesto,25.96',
                '2018-11-04,Kranj,23.65',
                '2018-11-04,Murska Sobota,23.55',
                '2018-11-05,Koper,28.48',
                '2018-11-05,Kranj,24.72',
                '2018-11-05,Murska Sobota,27.88',
                '2018-11-06,Murska Sobota,21.48',
                '2018-11-08,Koper,26.08',
                '2018-11-08,Maribor,22.08',
                '2018-11-08,Murska Sobota,28.28',
                '2018-11-10,Kranj,29.07',
                '2018-11-10,Maribor,26.5',
                '2018-11-10,Murska Sobota,23.03',
                '2018-11-11,Koper,22.11',
                '2018-11-11,Novo mesto,20.91',
                '2018-11-12,Ljubljana,29.9',
                '2018-11-12,Maribor,25.55',
                '2018-11-12,Murska Sobota,20.6',
                '2018-11-13,Murska Sobota,21.89',
                '2018-11-14,Koper,26.25',
                '2018-11-14,Ljubljana,27.49',
                '2018-11-16,Maribor,21.23',
                '2018-11-16,Murska Sobota,29.6',
                '2018-11-18,Murska Sobota,27.74',
                '2018-11-26,Murska Sobota,22.52',
                '2018-11-28,Koper,29.19',
                '2018-11-28,Ljubljana,23.62',
                '2018-11-28,Murska Sobota,25.53',
                '2018-11-29,Kranj,26.34',
                '2018-11-29,Ljubljana,28.13',
                '2018-12-01,Maribor,25.5',
                '2018-12-03,Novo mesto,22.18',
                '2018-12-04,Celje,20.32',
                '2018-12-04,Kranj,22.18',
                '2018-12-04,Maribor,29.91',
                '2018-12-05,Celje,23.26',
                '2018-12-05,Koper,28.73',
                '2018-12-05,Maribor,20.44',
                '2018-12-06,Kranj,24.81',
                '2018-12-06,Novo mesto,20.73',
                '2018-12-08,Murska Sobota,25.42',
                '2018-12-09,Ljubljana,25.77',
                '2018-12-10,Maribor,23.68',
                '2018-12-11,Novo mesto,20.25',
                '2018-12-12,Novo mesto,21.72',
                '2018-12-13,Novo mesto,25.08',
                '2018-12-15,Kranj,21.44',
                '2018-12-16,Murska Sobota,21.27',
                '2018-12-16,Novo mesto,24.42',
                '2018-12-18,Ljubljana,29.3',
                '2018-12-18,Novo mesto,28.57',
                '2018-12-19,Kranj,26.69',
                '2018-12-19,Ljubljana,27.07',
                '2018-12-19,Novo mesto,29.73',
                '2018-12-20,Kranj,28.86',
                '2018-12-20,Ljubljana,21.97',
                '2018-12-21,Novo mesto,25.39',
                '2018-12-22,Ljubljana,21.23',
                '2018-12-23,Murska Sobota,25.24',
                '2018-12-24,Maribor,20.95',
                '2018-12-24,Novo mesto,21.3',
                '2018-12-25,Celje,25.53',
                '2018-12-26,Celje,27.5',
                '2018-12-26,Maribor,25.08',
                '2018-12-26,Murska Sobota,29.91',
                '2018-12-27,Murska Sobota,25.16',
                '2018-12-28,Celje,21.34',
                '2018-12-28,Maribor,25.98',
                '2018-12-29,Kranj,25.9',
                '2018-12-29,Maribor,22.27',
                '2018-12-30,Celje,27.41',
                '2018-12-30,Ljubljana,22.4',
                '2019-01-01,Kranj,28.75',
                '2019-01-01,Maribor,22.93',
                '2019-01-03,Maribor,20.89',
                '2019-01-04,Celje,26.61',
                '2019-01-04,Maribor,27.92',
                '2019-01-05,Koper,20.06',
                '2019-01-05,Novo mesto,25.82',
                '2019-01-06,Maribor,26.44',
                '2019-01-07,Maribor,20.13',
                '2019-01-08,Ljubljana,20.98',
                '2019-01-10,Kranj,21.16',
                '2019-01-11,Celje,24.24',
                '2019-01-11,Ljubljana,27.59',
                '2019-01-13,Celje,22.78',
                '2019-01-13,Maribor,27.92',
                '2019-01-14,Koper,28.27',
                '2019-01-14,Ljubljana,24.7',
                '2019-01-14,Maribor,24.14',
                '2019-01-16,Ljubljana,23.5',
                '2019-01-16,Novo mesto,23.68',
                '2019-01-17,Celje,26.66',
                '2019-01-17,Maribor,22.37',
                '2019-01-17,Murska Sobota,25.9',
                '2019-01-18,Kranj,25.85',
                '2019-01-18,Maribor,28.31',
                '2019-01-19,Ljubljana,24.85',
                '2019-01-19,Murska Sobota,24.81',
                '2019-01-20,Kranj,25.63',
                '2019-01-20,Murska Sobota,27.43',
                '2019-01-21,Murska Sobota,27.85',
                '2019-01-22,Koper,23.85',
                '2019-01-23,Maribor,27.56',
                '2019-01-25,Koper,24.26',
                '2019-01-25,Novo mesto,27.97',
                '2019-01-26,Koper,24.89',
                '2019-01-26,Ljubljana,29.02',
                '2019-01-27,Koper,23.99',
                '2019-01-27,Murska Sobota,28.33',
                '2019-01-28,Koper,29.2',
                '2019-01-28,Ljubljana,22.24',
                '2019-01-28,Maribor,22.1',
                '2019-01-30,Celje,27.79',
                '2019-01-30,Ljubljana,21.0',
                '2019-01-30,Maribor,23.33',
                '2019-01-31,Murska Sobota,20.06',
                '2019-02-02,Celje,24.77',
                '2019-02-03,Ljubljana,28.29',
                '2019-02-06,Celje,20.32',
                '2019-02-06,Murska Sobota,23.35',
                '2019-02-07,Kranj,27.55',
                '2019-02-07,Murska Sobota,26.06',
                '2019-02-08,Kranj,25.58',
                '2019-02-08,Murska Sobota,21.65',
                '2019-02-09,Koper,28.31',
                '2019-02-09,Ljubljana,21.18',
                '2019-02-10,Koper,20.55',
                '2019-02-10,Maribor,20.85',
                '2019-02-11,Celje,23.49',
                '2019-02-12,Celje,23.8',
                '2019-02-13,Kranj,24.96',
                '2019-02-16,Murska Sobota,26.31',
                '2019-02-16,Novo mesto,22.16',
                '2019-02-17,Celje,29.37',
                '2019-02-17,Kranj,25.13',
                '2019-02-17,Ljubljana,26.65',
                '2019-02-17,Maribor,28.34',
                '2019-02-18,Kranj,24.9',
                '2019-02-19,Kranj,22.47',
                '2019-02-20,Celje,26.65',
                '2019-02-21,Celje,23.44',
                '2019-02-21,Koper,24.39',
                '2019-02-23,Novo mesto,29.28',
                '2019-02-25,Maribor,24.18',
                '2019-02-26,Ljubljana,25.86',
                '2019-02-27,Ljubljana,28.84',
                '2019-02-27,Maribor,24.6',
                '2019-02-28,Celje,27.08',
                '2019-02-28,Novo mesto,28.42',
                '2019-03-01,Celje,23.85',
                '2019-03-01,Maribor,28.78',
                '2019-03-02,Kranj,25.87',
                '2019-03-05,Koper,21.8',
                '2019-03-08,Koper,25.61',
                '2019-03-08,Murska Sobota,26.17',
                '2019-03-09,Ljubljana,20.33',
                '2019-03-09,Maribor,25.31',
                '2019-03-09,Novo mesto,27.53',
                '2019-03-11,Novo mesto,28.52',
                '2019-03-12,Koper,26.24',
                '2019-03-12,Ljubljana,25.34',
                '2019-03-13,Kranj,27.24',
                '2019-03-14,Murska Sobota,23.12',
                '2019-03-14,Novo mesto,20.55',
                '2019-03-15,Koper,25.31',
                '2019-03-16,Kranj,29.17',
                '2019-03-17,Celje,27.9',
                '2019-03-17,Koper,26.4',
                '2019-03-18,Kranj,21.18',
                '2019-03-19,Celje,25.32',
                '2019-03-20,Ljubljana,24.7',
                '2019-03-20,Novo mesto,22.92',
                '2019-03-21,Ljubljana,26.24',
                '2019-03-22,Kranj,21.82',
                '2019-03-23,Ljubljana,23.14',
                '2019-03-23,Maribor,20.71',
                '2019-03-24,Maribor,27.02',
                '2019-03-25,Kranj,26.54',
                '2019-03-25,Maribor,25.67',
                '2019-03-25,Murska Sobota,23.55',
                '2019-03-27,Maribor,27.58',
                '2019-03-28,Koper,27.24',
                '2019-03-28,Kranj,23.63',
                '2019-03-30,Murska Sobota,29.84',
                '2019-03-30,Novo mesto,29.98',
                '2019-03-31,Novo mesto,29.79',
                '2019-04-01,Novo mesto,20.49',
                '2019-04-02,Koper,23.39',
                '2019-04-03,Celje,22.26',
                '2019-04-03,Murska Sobota,21.33',
                '2019-04-04,Celje,20.6',
                '2019-04-04,Maribor,27.37',
                '2019-04-05,Koper,24.79',
                '2019-04-05,Kranj,27.67',
                '2019-04-06,Kranj,21.43',
                '2019-04-06,Maribor,20.64',
                '2019-04-07,Koper,20.1',
                '2019-04-09,Ljubljana,20.58',
                '2019-04-09,Maribor,28.18',
                '2019-04-11,Ljubljana,27.41',
                '2019-04-12,Kranj,21.05',
                '2019-04-12,Maribor,29.1',
                '2019-04-16,Celje,26.15',
                '2019-04-17,Ljubljana,28.15',
                '2019-04-18,Maribor,28.7',
                '2019-04-19,Koper,22.74',
                '2019-04-19,Kranj,25.16',
                '2019-04-21,Koper,29.62',
                '2019-04-21,Kranj,27.61',
                '2019-04-22,Ljubljana,25.14',
                '2019-04-24,Murska Sobota,26.37',
                '2019-04-26,Koper,29.46',
                '2019-04-26,Kranj,28.44',
                '2019-04-27,Maribor,23.38',
                '2019-04-28,Celje,21.22',
                '2019-04-28,Koper,24.07',
                '2019-04-28,Kranj,22.06',
                '2019-04-29,Maribor,24.43',
                '2019-04-29,Novo mesto,27.67',
                '2019-04-30,Maribor,24.23',
                '2019-04-30,Novo mesto,28.29',
                '2019-05-01,Koper,25.34',
                '2019-05-01,Kranj,20.2',
                '2019-05-02,Kranj,24.23',
                '2019-05-02,Ljubljana,20.78',
                '2019-05-03,Maribor,27.8',
                '2019-05-03,Novo mesto,21.47',
                '2019-05-04,Murska Sobota,29.52',
                '2019-05-04,Novo mesto,26.11',
                '2019-05-05,Ljubljana,25.68',
                '2019-05-06,Maribor,21.33',
                '2019-05-07,Koper,26.88',
                '2019-05-07,Murska Sobota,23.48',
                '2019-05-09,Ljubljana,25.86',
                '2019-05-10,Celje,23.48',
                '2019-05-11,Celje,20.99',
                '2019-05-11,Novo mesto,27.58',
                '2019-05-12,Kranj,21.29',
                '2019-05-13,Celje,26.02',
                '2019-05-13,Ljubljana,22.39',
                '2019-05-13,Maribor,25.63',
                '2019-05-15,Celje,26.8',
                '2019-05-15,Ljubljana,20.56',
                '2019-05-17,Kranj,20.45',
                '2019-05-18,Kranj,27.12',
                '2019-05-19,Koper,28.59',
                '2019-05-19,Maribor,22.53',
                '2019-05-19,Murska Sobota,27.03',
                '2019-05-20,Kranj,22.51',
                '2019-05-20,Murska Sobota,22.44',
                '2019-05-22,Maribor,26.5',
                '2019-05-23,Ljubljana,24.66',
                '2019-05-23,Maribor,26.12',
                '2019-05-24,Koper,24.76',
                '2019-05-24,Ljubljana,26.22',
                '2019-05-24,Novo mesto,23.93',
                '2019-05-26,Ljubljana,25.76',
                '2019-05-28,Kranj,21.84',
                '2019-05-28,Ljubljana,21.59',
                '2019-05-28,Maribor,29.9',
                '2019-05-30,Celje,28.89',
                '2019-05-31,Celje,21.26',
                '2019-05-31,Kranj,21.41',
                '2019-06-01,Kranj,25.35',
                '2019-06-01,Novo mesto,26.92',
                '2019-06-02,Celje,29.65',
                '2019-06-02,Murska Sobota,24.59',
                '2019-06-02,Novo mesto,22.42',
                '2019-06-05,Ljubljana,26.45',
                '2019-06-05,Novo mesto,27.66',
                '2019-06-06,Kranj,26.65',
                '2019-06-06,Ljubljana,29.34',
                '2019-06-07,Kranj,21.71',
                '2019-06-08,Novo mesto,25.26',
                '2019-06-09,Murska Sobota,28.74',
                '2019-06-09,Novo mesto,27.29',
                '2019-06-10,Novo mesto,26.99',
                '2019-06-12,Celje,21.79',
                '2019-06-12,Ljubljana,26.6',
                '2019-06-12,Murska Sobota,21.72',
                '2019-06-13,Koper,28.23',
                '2019-06-13,Maribor,28.86',
                '2019-06-15,Kranj,27.88',
                '2019-06-16,Murska Sobota,25.66',
                '2019-06-16,Novo mesto,26.51',
                '2019-06-17,Novo mesto,20.51',
                '2019-06-20,Maribor,23.2',
                '2019-06-21,Koper,26.89',
                '2019-06-21,Kranj,24.13',
                '2019-06-21,Murska Sobota,28.66',
                '2019-06-22,Koper,28.9',
                '2019-06-22,Murska Sobota,29.85',
                '2019-06-24,Celje,21.44',
                '2019-06-24,Kranj,23.21',
                '2019-06-24,Murska Sobota,22.62',
                '2019-06-25,Maribor,26.31',
                '2019-06-26,Ljubljana,25.65',
                '2019-06-26,Novo mesto,23.08',
                '2019-06-27,Koper,24.02',
                '2019-06-27,Ljubljana,26.85',
                '2019-07-01,Celje,24.11',
                '2019-07-01,Maribor,21.45',
                '2019-07-01,Novo mesto,29.73',
                '2019-07-02,Celje,26.58',
                '2019-07-02,Novo mesto,20.14',
                '2019-07-04,Ljubljana,20.19',
                '2019-07-04,Murska Sobota,27.19',
                '2019-07-05,Koper,29.0',
                '2019-07-05,Novo mesto,22.73',
                '2019-07-06,Novo mesto,23.05',
                '2019-07-07,Ljubljana,26.09',
                '2019-07-07,Novo mesto,26.65',
                '2019-07-08,Ljubljana,29.18',
                '2019-07-09,Kranj,22.1',
                '2019-07-09,Maribor,24.15',
                '2019-07-10,Maribor,20.49',
                '2019-07-10,Novo mesto,28.99',
                '2019-07-11,Koper,25.01',
                '2019-07-12,Murska Sobota,28.29',
                '2019-07-13,Ljubljana,26.06',
                '2019-07-14,Kranj,23.23',
                '2019-07-14,Murska Sobota,29.01',
                '2019-07-17,Celje,22.76',
                '2019-07-17,Maribor,22.46',
                '2019-07-17,Novo mesto,22.57',
                '2019-07-19,Celje,21.21',
                '2019-07-19,Koper,23.95',
                '2019-07-19,Ljubljana,23.24',
                '2019-07-20,Ljubljana,24.73',
                '2019-07-20,Maribor,26.85',
                '2019-07-21,Celje,21.18',
                '2019-07-21,Ljubljana,21.18',
                '2019-07-21,Murska Sobota,26.34',
                '2019-07-22,Maribor,22.56',
                '2019-07-22,Novo mesto,25.76',
                '2019-07-23,Koper,24.09',
                '2019-07-25,Murska Sobota,24.58',
                '2019-07-26,Koper,28.33',
                '2019-07-28,Celje,23.6',
                '2019-07-28,Koper,22.21',
                '2019-07-28,Maribor,24.72',
                '2019-07-28,Novo mesto,25.28',
                '2019-07-31,Maribor,23.57',
                '2019-08-02,Koper,28.58',
                '2019-08-02,Novo mesto,21.69',
                '2019-08-03,Kranj,29.33',
                '2019-08-03,Ljubljana,26.76',
                '2019-08-03,Maribor,28.52',
                '2019-08-05,Ljubljana,22.93',
                '2019-08-06,Novo mesto,25.16',
                '2019-08-07,Koper,27.45',
                '2019-08-07,Ljubljana,26.17',
                '2019-08-08,Murska Sobota,25.79',
                '2019-08-09,Kranj,29.64',
                '2019-08-09,Maribor,28.54',
                '2019-08-09,Novo mesto,23.4',
                '2019-08-10,Maribor,23.15',
                '2019-08-11,Koper,28.62',
                '2019-08-11,Murska Sobota,25.55',
                '2019-08-12,Koper,22.18',
                '2019-08-13,Kranj,22.8',
                '2019-08-14,Koper,24.27',
                '2019-08-14,Maribor,21.85',
                '2019-08-15,Kranj,25.57',
                '2019-08-15,Novo mesto,29.43',
                '2019-08-16,Kranj,22.07',
                '2019-08-16,Ljubljana,23.71',
                '2019-08-16,Novo mesto,27.12',
                '2019-08-17,Celje,29.7',
                '2019-08-17,Koper,23.09',
                '2019-08-17,Murska Sobota,21.89',
                '2019-08-19,Celje,20.48',
                '2019-08-19,Murska Sobota,20.19',
                '2019-08-20,Ljubljana,25.54',
                '2019-08-21,Novo mesto,26.37',
                '2019-08-22,Kranj,26.35',
                '2019-08-23,Celje,28.68',
                '2019-08-24,Celje,25.86',
                '2019-08-24,Koper,25.57',
                '2019-08-26,Kranj,23.04',
                '2019-08-26,Ljubljana,20.08',
                '2019-08-26,Maribor,20.61',
                '2019-08-27,Celje,28.29',
                '2019-08-27,Novo mesto,22.59',
                '2019-08-28,Koper,22.99',
                '2019-08-28,Ljubljana,23.96',
                '2019-08-29,Koper,26.05',
                '2019-08-30,Novo mesto,20.03',
                '2019-09-01,Murska Sobota,21.58',
                '2019-09-03,Koper,26.14',
                '2019-09-03,Maribor,27.07',
                '2019-09-05,Kranj,27.51',
                '2019-09-05,Novo mesto,20.05',
                '2019-09-06,Koper,29.41',
                '2019-09-06,Maribor,24.1',
                '2019-09-06,Murska Sobota,24.66',
                '2019-09-07,Maribor,22.52',
                '2019-09-07,Murska Sobota,23.22',
                '2019-09-08,Murska Sobota,29.5',
                '2019-09-10,Koper,29.21',
                '2019-09-11,Celje,26.41',
                '2019-09-13,Celje,26.12',
                '2019-09-13,Koper,29.73',
                '2019-09-13,Ljubljana,29.45',
                '2019-09-14,Novo mesto,20.93',
                '2019-09-17,Koper,26.87',
                '2019-09-17,Ljubljana,29.24',
                '2019-09-17,Murska Sobota,21.08',
                '2019-09-19,Celje,27.99',
                '2019-09-19,Ljubljana,25.98',
                '2019-09-21,Celje,22.9',
                '2019-09-22,Celje,26.28',
                '2019-09-22,Novo mesto,21.59',
                '2019-09-23,Celje,25.95',
                '2019-09-24,Kranj,25.63',
                '2019-09-24,Murska Sobota,22.12',
                '2019-09-24,Novo mesto,25.0',
                '2019-09-26,Koper,22.73',
                '2019-09-27,Kranj,29.0',
                '2019-09-28,Maribor,25.9',
                '2019-09-28,Novo mesto,21.28',
                '2019-09-29,Koper,25.79',
                '2019-09-29,Ljubljana,28.83',
                '2019-09-30,Murska Sobota,28.23',
                '2019-09-30,Novo mesto,29.05',
                '2019-10-02,Ljubljana,22.71',
                '2019-10-03,Koper,28.71',
                '2019-10-03,Maribor,26.4',
                '2019-10-03,Novo mesto,25.65',
                '2019-10-05,Ljubljana,24.03',
                '2019-10-06,Kranj,27.3',
                '2019-10-07,Celje,28.3',
                '2019-10-07,Kranj,20.4',
                '2019-10-07,Murska Sobota,27.2',
                '2019-10-08,Celje,24.25',
                '2019-10-08,Kranj,28.0',
                '2019-10-11,Koper,27.01',
                '2019-10-11,Ljubljana,21.13',
                '2019-10-12,Maribor,26.57',
                '2019-10-13,Celje,29.14',
                '2019-10-13,Murska Sobota,25.58',
                '2019-10-14,Ljubljana,21.29',
                '2019-10-16,Maribor,29.84',
                '2019-10-16,Murska Sobota,22.79',
                '2019-10-17,Koper,22.44',
                '2019-10-20,Celje,26.26',
                '2019-10-20,Koper,23.62',
                '2019-10-20,Novo mesto,26.33',
                '2019-10-21,Celje,23.07',
                '2019-10-21,Kranj,27.2',
                '2019-10-21,Ljubljana,23.37',
                '2019-10-23,Celje,24.71',
                '2019-10-23,Kranj,22.34',
                '2019-10-23,Maribor,24.5',
                '2019-10-25,Ljubljana,21.81',
                '2019-10-25,Maribor,24.21',
                '2019-10-25,Murska Sobota,20.74',
                '2019-10-27,Maribor,28.92',
                '2019-10-27,Murska Sobota,27.35',
                '2019-10-29,Celje,22.16',
                '2019-10-31,Ljubljana,20.48',
                '2019-10-31,Maribor,22.11',
                '2019-11-01,Kranj,28.43',
                '2019-11-02,Koper,26.98',
                '2019-11-03,Celje,20.13',
                '2019-11-03,Maribor,24.24',
                '2019-11-03,Novo mesto,28.4',
                '2019-11-04,Murska Sobota,20.33',
                '2019-11-05,Murska Sobota,27.36',
                '2019-11-05,Novo mesto,22.39',
                '2019-11-06,Kranj,20.92',
                '2019-11-06,Ljubljana,22.72',
                '2019-11-09,Novo mesto,25.27',
                '2019-11-10,Koper,29.95',
                '2019-11-10,Kranj,20.94',
                '2019-11-11,Celje,28.95',
                '2019-11-11,Ljubljana,29.49',
                '2019-11-13,Celje,20.18',
                '2019-11-13,Maribor,25.1',
                '2019-11-14,Celje,21.78',
                '2019-11-15,Celje,28.97',
                '2019-11-15,Murska Sobota,25.97',
                '2019-11-15,Novo mesto,20.09',
                '2019-11-16,Maribor,22.83',
                '2019-11-16,Murska Sobota,22.54',
                '2019-11-16,Novo mesto,26.19',
                '2019-11-17,Murska Sobota,28.36',
                '2019-11-18,Kranj,27.95',
                '2019-11-18,Maribor,21.28',
                '2019-11-18,Murska Sobota,25.07',
                '2019-11-19,Celje,23.37',
                '2019-11-20,Celje,27.29',
                '2019-11-20,Koper,28.26',
                '2019-11-21,Novo mesto,21.81',
                '2019-11-22,Maribor,21.38',
                '2019-11-23,Celje,28.97',
                '2019-11-24,Ljubljana,29.99',
                '2019-11-25,Celje,23.19',
                '2019-11-25,Koper,22.79',
                '2019-11-25,Kranj,26.16',
                '2019-11-25,Novo mesto,22.85',
                '2019-11-26,Celje,21.91',
                '2019-11-26,Murska Sobota,23.51',
                '2019-11-27,Novo mesto,20.92',
                '2019-11-28,Celje,21.54',
                '2019-11-28,Kranj,26.43',
                '2019-11-28,Maribor,23.14',
                '2019-11-29,Kranj,23.69',
                '2019-11-30,Novo mesto,24.24',
                '2019-12-01,Kranj,23.39',
                '2019-12-04,Celje,28.75',
                '2019-12-06,Koper,20.74',
                '2019-12-06,Ljubljana,24.31',
                '2019-12-07,Maribor,23.25',
                '2019-12-10,Maribor,24.7',
                '2019-12-11,Celje,20.5',
                '2019-12-12,Ljubljana,25.67',
                '2019-12-13,Koper,22.72',
                '2019-12-14,Ljubljana,28.15',
                '2019-12-15,Maribor,25.41',
                '2019-12-19,Celje,24.1',
                '2019-12-21,Celje,25.54',
                '2019-12-21,Ljubljana,29.77',
                '2019-12-21,Murska Sobota,27.23',
                '2019-12-22,Celje,23.16',
                '2019-12-22,Koper,26.27',
                '2019-12-22,Murska Sobota,26.9',
                '2019-12-23,Novo mesto,22.56',
                '2019-12-26,Koper,25.48',
                '2019-12-27,Maribor,28.38',
                '2019-12-28,Celje,23.28',
                '2019-12-28,Koper,29.69',
                '2019-12-28,Novo mesto,28.71',
                '2019-12-29,Ljubljana,23.21',
                '2019-12-30,Koper,20.22',
                '2019-12-30,Kranj,23.35',
                '2019-12-31,Kranj,27.46'
            ]
            test_cases = [
                ('out1.txt', ['Celje,24.29', 'Koper,27.01', 'Kranj,24.82', 'Ljubljana,26.98', 'Maribor,26.12', 'Murska Sobota,25.98', 'Novo mesto,25.18'], '2019-06-01', '2019-06-30'),
                ('out2.txt', ['Celje,25.09', 'Koper,25.19', 'Kranj,25.07', 'Ljubljana,25.12', 'Maribor,24.95', 'Murska Sobota,25.33', 'Novo mesto,24.66', 'Ptuj,25.00'], '2018-01-01', '2019-12-31'),
            ]
            with Check.in_file("meritve.txt", podatki, encoding='utf-8'):
                for out_name, izhod, zacetek, konec in test_cases:
                    meritve("meritve.txt", out_name, zacetek, konec)
                    if not Check.out_file(out_name, izhod, encoding='utf-8'):
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
