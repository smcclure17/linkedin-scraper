from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, List, Set, Union

from libs.linkedin_client import LinkedInClient
from libs import utils

# Retrive LinkedIn account info from local system environment.
# TODO: Make this optional? Pass args through invoke task? 
# idk, but I don't like this
USERNAME = utils.get_env_variable("LINKEDIN_USER")
PASSWORD = utils.get_env_variable("LINKEDIN_PASS")


@dataclass(frozen=True)
class Alum:
    """Personal data pulled from an Alum's LinkedIn page."""

    id: str
    url: str
    name: str
    # We could grab employment history, but for now just grab current info.
    company: Union[str, None]
    title: Union[str, None]
    industry: Union[str, None]
    graduation_year: Union[str, None]
    major: Union[str, None]
    location: Union[str, None]

    @classmethod
    def from_id(self, id: str) -> "Alum":
        # I envisioned these being class properties but dataclasses.asdict()
        # does not recognize properties for serialization :(
        url = f"https://linkedin.com/in/{id}"
        payload = _make_user_request(user_id=id)
        profile: Dict = payload["profile"]
        education: Dict = payload["educationView"]
        employment: Dict = payload["positionGroupView"]

        # An alum should always have Wheaton in their education, but if not handle that here
        try:
            wheaton: Dict = [
                school
                for school in education["elements"]
                if school["schoolUrn"] == "urn:li:fs_miniSchool:20143"
            ][0]
        except KeyError:
            wheaton: Dict = {}

        # Probably need to error check that all these nests actually exist
        return Alum(
            id=id,
            url=url,
            name=f"{profile['firstName']} {profile['lastName']}",
            industry=profile.get("industryName"),
            location=profile.get("geoLocationName"),
            company=employment["elements"][0]["name"],
            title=employment["elements"][0]["positions"][0]["title"],
            graduation_year=wheaton.get("timePeriod")
            .get("endDate")
            .get("year"),  # God I hate this syntax
            major=wheaton["fieldOfStudy"],
        )

    @classmethod
    def from_url(self, url: str) -> "Alum":
        # Light assumption that url is sanitary, e.g.
        # https://www.linkedin.com/in/user-id-123/
        id = url.split("linkedin.com/in/")[1].replace("/", "")
        return Alum.from_id(id=id)


@lru_cache
def _make_user_request(user_id: str, client=None) -> Set[Dict[str, Any]]:
    if client is None:
        client = LinkedInClient.from_user(username=USERNAME, password=PASSWORD)

    return client.session.get(
        f"https://www.linkedin.com/voyager/api/identity/profiles/{user_id}/profileView",
        headers=LinkedInClient.REQUEST_HEADERS,
    ).json()
