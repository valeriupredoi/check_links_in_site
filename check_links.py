import urllib.error as uerr
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


ignore_links = ["http://foundation.zurb.com/"]

# mainfunc
def _check_site(site, site_prefix):
    """Check if links inside provided links are active."""
    # main links
    main_links = _get_main_links(site)

    # exit if empty
    if not main_links:
        raise ValueError("Main links empy; site may be down!")

    # filter links
    filtered_main_links = _filter(main_links)

    # loop through branches
    for sub_link in filtered_main_links:
        _test_link(sub_link)

        # test sub-sub-links only if they belong to the site
        if site_prefix in sub_link:
            links = _get_main_links(sub_link)
            filtered_links = _filter(links)
            # exit if empty
            if not filtered_links:
                raise ValueError("Main links empy; site may be down!")

            # test links
            for link in filtered_links:
                if link not in filtered_main_links:
                    _test_link(link)


def _get_main_links(site):
    """Grab the main links of the site."""
    req = Request(site)
    pages = urlopen(req)
    soup = BeautifulSoup(pages, 'html.parser')
    all_links = []

    # grab all links
    for link in soup.findAll('a'):
        all_links.append(link.get('href'))

    return all_links


def _filter(links_list):
    """Pass a links list for filtering."""
    filtered_links = [l for l in links_list if l is not None]
    filtered_links = [l for l in filtered_links if len(l) > 4]
    filtered_links = [l for l in filtered_links if l.startswith("http")]

    return filtered_links


def _test_link(link):
    """Test link for activity."""
    if link in ignore_links:
        return
    # print(f"Examining {link}")
    try:
        code = urlopen(link).getcode()
        if code != 200:
            print(f"WARNING: {link} accessible but code is not 200!")
    except uerr.HTTPError as exc:
        print(f"WARNING: {link} gives {exc}")


# run routine
# pass the site you need checking as first arg
# pass the prefix of secondary links as second arg
_check_site("https://is-enes3.github.io/IS-ENES-Website/",
            "https://is-enes3.github.io/IS-ENES-Website/")
