import inspect
from typing import get_type_hints
from collections import abc


DEBUG = False


class VarDecl:

    def ctrl(this, is_classe: bool = False):
        this.is_classe = is_classe

        def fonction(methode, *args):
            typehints = get_type_hints(methode)
            this.kwparams = typehints
            if DEBUG:
                print(this.kwparams, end="")

            this.params = [this.kwparams[k] for k in this.kwparams]
            this.nombre_params = len(this.kwparams)
            # print("this:", this.nombre_params, kwparams)

            def parametres(*args, **kwargs):
                nb_params = 0
                nb_params += this.nombre_params
                if args:
                    # print("args:", nb_params, "=", args, kwargs)

                    # Ne pas prendre le 1er item de la liste si c'est une classe
                    debut = 1 if this.is_classe else 0
                    for i, arg in enumerate(args[debut:]):
                        # print(" ", i, "arg:", arg, nb_params)
                        if i >= nb_params:
                            # print(i, "params:", this.kwparams)
                            # print(nb_params, "args:", arg, args)
                            if nb_params > 0:
                                raise TypeError(f"Trop de parametres: {1+i} sur {nb_params} attendus")
                        else:
                            def_params = this.params[i]
                            if not def_params:
                                # print("    param:", arg, "inconnu")
                                continue

                        # print("def_params:", def_params)
                        if def_params.__class__ in [tuple, list]:
                            definition = []
                            for parami in def_params:
                                definition.append(parami.__name__)
                        # elif def_params in [P.args]:
                        elif def_params in [tARGS]:
                            nb_params = 0
                            continue
                        else:
                            definition = [def_params.__name__]

                        controle = arg.__class__.__name__
                        if controle not in definition:
                            if len(definition) == 1:
                                definition = definition[0]
                            iemestr = "er" if i == 0 else "ème"
                            message = f"Appel de {methode.__qualname__}(), {1+i}{iemestr} argument ({arg!r}) de type '{controle}' au lieu de '{definition}'"
                            raise TypeError(message)

                if kwargs:
                    # print("kwargs:", kwargs)
                    for kwarg in kwargs:
                        definition = this.kwparams.get(kwarg)
                        # print("  kwarg:", kwarg, "=", kwargs[kwarg], definition)
                        if not definition:
                            # print(">", kwarg, [this.kwparams[un_type].__name__ for un_type in this.kwparams]) 
                            if tKWARGS not in [this.kwparams[un_type] for un_type in this.kwparams]:
                                message = f"Appel de {methode.__qualname__}() : Parametre '{kwarg}' non défini"
                                raise TypeError(message)
                            continue
                        
                        definition = definition.__name__
                        controle = kwargs[kwarg].__class__.__name__
                        if definition != controle:
                            message = f"Appel de {methode.__qualname__}() : Le paramètre '{kwarg}' est de type '{controle}' au lieu de '{definition}'"
                            raise TypeError(message)

                return methode(*args, **kwargs)
            return parametres
        return fonction


class MethodesDico(abc.MutableMapping):

    def __init__(self, *args, **kwargs):
        self.dico = dict(*args, **kwargs)

    def __getitem__(self, key):
        valeur = self.dico[key]["VALUE"]
        if DEBUG:        
            # params = self.dico[key]["PARAMS"]
            # print(f"< get {key:15} =", valeur.__class__)
            pass
        return valeur

    def __setitem__(self, key, value):
        est_fonction = inspect.isfunction(value)
        if DEBUG:
            print(end=">" if est_fonction else "x")
            print(f" set {key:15} to: ", end="")
            print(f"{value.__qualname__}(" if inspect.isfunction(value) else value, end="")

        if est_fonction:
            self.dico[key] = {}
            # typehints = get_type_hints(value, globalns=False, localns=False, include_extras=False)
            # self.dico[key]["PARAMS"] = typehints
            self.dico[key]["VALUE"] = VarDecl().ctrl(True)(value)

            if DEBUG:        
                print(")")

        elif DEBUG:        
            print("")

    def __delitem__(self, key):
        if DEBUG:
            print("x del:", key)

    def __iter__(self):
        # print("  .. iter()")
        return iter(self.dico)

    def __len__(self):
        if DEBUG:
            print("[] len()")
        return 0


class tARGS(type):
    pass


class tKWARGS(type):
    pass


class VarDeclCtrlMeta(type):

    def __init__(self, *args):
        # print(args)
        pass

    def __prepare__(cls, *args, **kwargs):
        if DEBUG:
            print("\nPreparation", args, kwargs, end=": ")
        res = MethodesDico()
        if DEBUG:
            print("Ok")
        return res

    def __new__(cls, name, bases, methodes: MethodesDico):
        if False and DEBUG:
            list_classes = "(" + ", ".join([c.__name__ for c in bases]) + ")"
            print("class", f"{name}{list_classes}:")
            for dico in methodes:
                print(f"  - {name}: {dico}")
            print()

        return super().__new__(cls, name, bases, dict(methodes))

    def __call__(self, *args, **kwargs):
        if DEBUG:
            print("Instantiate class", self.__name__, "with", args, kwargs)
        return super().__call__(*args, **kwargs)


# @VarDecl().ctrl()
# def maFonc(a: int, b: str):
#     print(a, b)

