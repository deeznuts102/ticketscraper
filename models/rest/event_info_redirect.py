from __future__ import annotations

from pydantic import BaseModel, Field

class SingleEntranceType(BaseModel):
    id: str
    slug: str
    path: str

class PagePropsRedirect(BaseModel):
    redirect_url: str = Field(..., alias='__N_REDIRECT')

class EventInfoRedirect(BaseModel):
    page_props: PagePropsRedirect = Field(..., alias='pageProps')

    def get_entrance_type(self) -> SingleEntranceType:
        """ Parse the redirect URL and return a SingleEntranceType instance

        Returns:
            SingleEntranceType: Contains information necessary to request Ticket information
        """
        redirect_url = self.page_props.redirect_url
        id = redirect_url.split('/')[-1]
        slug = redirect_url.split('/')[-3]

        return SingleEntranceType(
            id=id,
            slug=slug,
            path=redirect_url
        )
