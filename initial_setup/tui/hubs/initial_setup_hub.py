from pyanaconda.ui.tui.hubs import TUIHub
from pyanaconda.ui.tui.spokes import TUISpoke
from pyanaconda.ui.common import collect
from initial_setup import product
import os

__all__ = ["InitialSetupMainHub"]

# localization
_ = lambda t: t
N_ = lambda t: t

def collect_spokes(mask_paths):
    """Return a list of all spoke subclasses that should appear for a given
       category. Look for them in files imported as module_path % basename(f)

       :param mask_paths: list of mask, path tuples to search for classes
       :type mask_paths: list of (mask, path)

       :return: list of Spoke classes belonging to category
       :rtype: list of Spoke classes

    """
    spokes = []
    for mask, path in mask_paths:
        spokes.extend(collect(mask, path,
                              lambda obj: issubclass(obj, Spoke) and obj.should_run("firstboot", None)))

    return spokes


class InitialSetupMainHub(TUIHub):
    categories = ["password", "localization"]

    prod_title = product.product_title()
    if prod_title:
        title = _("Initial setup of %(product)s") % {"product": prod_title}
    else:
        title = _("Initial setup")

    def _collectCategoriesAndSpokes(self):
        """collects categories and spokes to be displayed on this Hub

           :return: dictionary mapping category class to list of spoke classes
           :rtype: dictionary[category class] -> [ list of spoke classes ]
        """

        ret = {}

        # Collect all the categories this hub displays, then collect all the
        # spokes belonging to all those categories.
        candidate_spokes = collect_spokes(self.paths["spokes"])
        spokes = [spoke for spoke in candidate_spokes \
                        if spoke.should_run("firstboot", self.data)]

        for spoke in spokes:
            ret.setdefault(spoke.category, [])
            ret[spoke.category].append(spoke)

        return ret