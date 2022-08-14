from typing import Dict, List
import requests  # type: ignore
import json

from models.event import Event
from models.festival_season_event import FestivalSeasonEvent
from models.nearby_events import TicketswapApiResponseNearbyEvents
from models.reserved_listings import TicketswapApiResponseEvent
from models.structured_event_data import StructuredEventResponse

GRAPHQL_URL = "https://api.ticketswap.com/graphql/public?"


def get_nearby_events() -> List[str]:
    payload = json.dumps(
        [
            {
                "operationName": "nearby",
                "variables": {"latitude": 52.3647, "longitude": 6.6842},
                "query": "query nearby($latitude: Float, $longitude: Float) {\n  nearby(latitude: $latitude, longitude: $longitude) {\n    risingEvents(first: 8) {\n      id\n      name\n      startDate\n      imageUrl\n      slug\n      availableTicketsCount\n      location {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    popularLocations(first: 6) {\n      id\n      slug\n      image\n      name\n      background\n      __typename\n    }\n    __typename\n  }\n}\n",
            },
            {
                "operationName": "getTestimonials",
                "variables": {
                    "first": 3,
                    "language": "en",
                    "minimumRating": 4,
                    "minimumLength": 5,
                    "maximumLength": 200,
                },
                "query": "query getTestimonials($first: Int, $language: String!, $minimumRating: Int, $minimumLength: Int, $maximumLength: Int, $after: String) {\n  testimonials(\n    first: $first\n    after: $after\n    language: $language\n    minimumRating: $minimumRating\n    minimumLength: $minimumLength\n    maximumLength: $maximumLength\n  ) {\n    edges {\n      node {\n        ... on Testimonial {\n          id\n          rating\n          user {\n            id\n            avatar\n            firstname\n            __typename\n          }\n          description\n          createdAt\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    totalReviewCount\n    reviewAverage\n    pageInfo {\n      hasNextPage\n      endCursor\n      __typename\n    }\n    __typename\n  }\n}\n",
            },
            {
                "operationName": "getUsercountAndAvatars",
                "variables": {},
                "query": "query getUsercountAndAvatars {\n  randomUserAvatars(first: 90) {\n    avatar\n    __typename\n  }\n  userCount\n}\n",
            },
            {
                "operationName": "LoggedInUserKycStatus",
                "variables": {},
                "query": "query LoggedInUserKycStatus {\n  loggedInUser {\n    id\n    knowYourCustomer {\n      status\n      __typename\n    }\n    __typename\n  }\n}\n",
            },
            {
                "operationName": "getFeedItems",
                "variables": {"countryCode": "NL"},
                "query": "query getFeedItems($countryCode: CountryCode) {\n  explore(countryCode: $countryCode) {\n    feed(first: 20) {\n      edges {\n        node {\n          ...thumbnailBlog\n          ...thumbnailEventCollection\n          ...thumbnailWithUrl\n          ...groupCollection\n          ...recurringEventCollection\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment thumbnailBlog on ThumbnailBlog {\n  id\n  type\n  status\n  blogPost {\n    id\n    title\n    subtitle\n    imageUrl\n    body\n    slug\n    author {\n      id\n      firstname\n      __typename\n    }\n    createdAt\n    __typename\n  }\n  __typename\n}\n\nfragment thumbnailEventCollection on ThumbnailEventCollection {\n  id\n  type\n  status\n  title\n  subtitle\n  group {\n    ...group\n    __typename\n  }\n  __typename\n}\n\nfragment group on Group {\n  id\n  subtitle\n  title\n  imageBackgroundUrl\n  imageThumbnailUrl\n  logoUrl\n  items(first: 100) {\n    edges {\n      node {\n        ...eventList\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment eventList on Event {\n  id\n  slug\n  name\n  isHighlighted\n  imageUrl\n  category\n  startDate\n  endDate\n  availableTicketsCount\n  status\n  artists {\n    ...artist\n    __typename\n  }\n  country {\n    ...country\n    __typename\n  }\n  uri {\n    path\n    __typename\n  }\n  location {\n    id\n    name\n    city {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment artist on Artist {\n  id\n  name\n  slug\n  avatar\n  numberOfUpcomingEvents\n  isFollowedByViewer\n  viewerHasNotificationsEnabled\n  __typename\n}\n\nfragment country on Country {\n  name\n  code\n  __typename\n}\n\nfragment thumbnailWithUrl on ThumbnailWithUrl {\n  id\n  type\n  status\n  title\n  subtitle\n  url\n  imageUrl\n  __typename\n}\n\nfragment groupCollection on GroupCollection {\n  id\n  type\n  status\n  title\n  subtitle\n  numberOfItemsOnFeedOverview: numbersOfItemsOnFeedOverview\n  group {\n    ...group\n    __typename\n  }\n  __typename\n}\n\nfragment recurringEventCollection on RecurringEventCollection {\n  id\n  type\n  status\n  title\n  subtitle\n  numberOfEventsOnFeedOverview: numbersOfEventsOnFeedOverview\n  imageBackgroundUrl: imageUrl\n  events {\n    edges {\n      node {\n        ...eventList\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n",
            },
            {
                "operationName": "getFollowedArtistsEvents",
                "variables": {"longitude": 6.6842, "latitude": 52.3647, "first": 10},
                "query": "query getFollowedArtistsEvents($first: Int, $latitude: Float, $longitude: Float) {\n  nearby(latitude: $latitude, longitude: $longitude) {\n    eventsByFollowedArtists(first: $first) {\n      edges {\n        node {\n          ...eventList\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  loggedInUser {\n    id\n    followedArtists(first: 8) {\n      ...followedArtists\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment eventList on Event {\n  id\n  slug\n  name\n  isHighlighted\n  imageUrl\n  category\n  startDate\n  endDate\n  availableTicketsCount\n  status\n  artists {\n    ...artist\n    __typename\n  }\n  country {\n    ...country\n    __typename\n  }\n  uri {\n    path\n    __typename\n  }\n  location {\n    id\n    name\n    city {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment artist on Artist {\n  id\n  name\n  slug\n  avatar\n  numberOfUpcomingEvents\n  isFollowedByViewer\n  viewerHasNotificationsEnabled\n  __typename\n}\n\nfragment country on Country {\n  name\n  code\n  __typename\n}\n\nfragment followedArtists on ArtistConnection {\n  edges {\n    node {\n      id\n      avatar\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n",
            },
        ]
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Accept": "*/*",
        "Accept-Language": "en",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.ticketswap.com/",
        "content-type": "application/json",
        "Origin": "https://www.ticketswap.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "TE": "trailers",
    }

    response = requests.request("POST", GRAPHQL_URL, headers=headers, data=payload)

    return json.loads(response.text)


def get_event_structure_data(event_id: str) -> List[str]:
    payload = json.dumps(
        [
            {
                "operationName": "getEventStructuredData",
                "variables": {"id": event_id},
                "query": "query getEventStructuredData($id: ID!) {\n  node(id: $id) {\n    ... on Event {\n      id\n      name\n      status\n      uri {\n        url\n        __typename\n      }\n      lowestPrice {\n        ...money\n        __typename\n      }\n      artists {\n        id\n        name\n        __typename\n      }\n      organizerBrands {\n        id\n        name\n        __typename\n      }\n      startDate\n      endDate\n      availableTicketsCount\n      location {\n        id\n        uri {\n          url\n          __typename\n        }\n        address\n        zipcode\n        name\n        city {\n          id\n          name\n          __typename\n        }\n        country {\n          ...country\n          __typename\n        }\n        __typename\n      }\n      types(first: 99) {\n        edges {\n          node {\n            id\n            availableListings: listings(first: 5, filter: {listingStatus: AVAILABLE}) {\n              edges {\n                node {\n                  id\n                  createdAt\n                  price {\n                    totalPriceWithTransactionFee {\n                      ...money\n                      __typename\n                    }\n                    __typename\n                  }\n                  uri {\n                    url\n                    __typename\n                  }\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment money on Money {\n  amount\n  currency\n  __typename\n}\n\nfragment country on Country {\n  name\n  code\n  __typename\n}\n",
            },
            {
                "operationName": "getTestimonials",
                "variables": {
                    "first": 3,
                    "language": "en",
                    "minimumRating": 4,
                    "minimumLength": 5,
                    "maximumLength": 200,
                },
                "query": "query getTestimonials($first: Int, $language: String!, $minimumRating: Int, $minimumLength: Int, $maximumLength: Int, $after: String) {\n  testimonials(\n    first: $first\n    after: $after\n    language: $language\n    minimumRating: $minimumRating\n    minimumLength: $minimumLength\n    maximumLength: $maximumLength\n  ) {\n    edges {\n      node {\n        ... on Testimonial {\n          id\n          rating\n          user {\n            id\n            avatar\n            firstname\n            __typename\n          }\n          description\n          createdAt\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    totalReviewCount\n    reviewAverage\n    pageInfo {\n      hasNextPage\n      endCursor\n      __typename\n    }\n    __typename\n  }\n}\n",
            },
            {
                "operationName": "getUsercountAndAvatars",
                "variables": {},
                "query": "query getUsercountAndAvatars {\n  randomUserAvatars(first: 90) {\n    avatar\n    __typename\n  }\n  userCount\n}\n",
            },
        ]
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Accept": "*/*",
        "Accept-Language": "en",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.ticketswap.com/",
        "content-type": "application/json",
        "Origin": "https://www.ticketswap.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "TE": "trailers",
    }

    response = requests.request("POST", GRAPHQL_URL, headers=headers, data=payload)

    return json.loads(response.text)


def get_reserved_listings(event_id: str) -> List[str]:
    payload = json.dumps(
        [
            {
                "operationName": "getReservedListings",
                "variables": {"id": f"{event_id}", "first": 10},
                "query": "query getReservedListings($id: ID!, $first: Int, $after: String) {\n  node(id: $id) {\n    ... on EventType {\n      id\n      slug\n      title\n      reservedListings: listings(\n        first: $first\n        filter: {listingStatus: RESERVED}\n        after: $after\n      ) {\n        ...listings\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment listings on ListingConnection {\n  edges {\n    node {\n      ...listingList\n      __typename\n    }\n    __typename\n  }\n  pageInfo {\n    endCursor\n    hasNextPage\n    __typename\n  }\n  __typename\n}\n\nfragment listingList on PublicListing {\n  id\n  hash\n  description\n  isPublic\n  status\n  dateRange {\n    startDate\n    endDate\n    __typename\n  }\n  uri {\n    path\n    __typename\n  }\n  event {\n    id\n    name\n    startDate\n    endDate\n    slug\n    status\n    location {\n      id\n      name\n      city {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  eventType {\n    id\n    title\n    startDate\n    endDate\n    __typename\n  }\n  seller {\n    id\n    firstname\n    avatar\n    __typename\n  }\n  tickets(first: 99) {\n    edges {\n      node {\n        id\n        status\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  numberOfTicketsInListing\n  numberOfTicketsStillForSale\n  price {\n    originalPrice {\n      ...money\n      __typename\n    }\n    totalPriceWithTransactionFee {\n      ...money\n      __typename\n    }\n    sellerPrice {\n      ...money\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment money on Money {\n  amount\n  currency\n  __typename\n}\n",
            },
            {
                "operationName": "getSoldListings",
                "variables": {"id": f"{event_id}"},
                "query": "query getSoldListings($id: ID!, $after: String) {\n  node(id: $id) {\n    ... on EventType {\n      id\n      slug\n      title\n      soldListings: listings(first: 3, filter: {listingStatus: SOLD}, after: $after) {\n        ...listings\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment listings on ListingConnection {\n  edges {\n    node {\n      ...listingList\n      __typename\n    }\n    __typename\n  }\n  pageInfo {\n    endCursor\n    hasNextPage\n    __typename\n  }\n  __typename\n}\n\nfragment listingList on PublicListing {\n  id\n  hash\n  description\n  isPublic\n  status\n  dateRange {\n    startDate\n    endDate\n    __typename\n  }\n  uri {\n    path\n    __typename\n  }\n  event {\n    id\n    name\n    startDate\n    endDate\n    slug\n    status\n    location {\n      id\n      name\n      city {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  eventType {\n    id\n    title\n    startDate\n    endDate\n    __typename\n  }\n  seller {\n    id\n    firstname\n    avatar\n    __typename\n  }\n  tickets(first: 99) {\n    edges {\n      node {\n        id\n        status\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  numberOfTicketsInListing\n  numberOfTicketsStillForSale\n  price {\n    originalPrice {\n      ...money\n      __typename\n    }\n    totalPriceWithTransactionFee {\n      ...money\n      __typename\n    }\n    sellerPrice {\n      ...money\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment money on Money {\n  amount\n  currency\n  __typename\n}\n",
            },
        ]
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Accept": "*/*",
        "Accept-Language": "en",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.ticketswap.com/",
        "content-type": "application/json",
        "authorization": "",
        "Origin": "https://www.ticketswap.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "TE": "trailers",
    }

    response = requests.request("POST", GRAPHQL_URL, headers=headers, data=payload)

    return json.loads(response.text)


def parse_nearby_events(res_json: List[Dict]) -> TicketswapApiResponseNearbyEvents:
    return TicketswapApiResponseNearbyEvents(**{"data": res_json})


def parse_festival_season_events(res_json: List[Dict]) -> List[FestivalSeasonEvent]:
    models: List[FestivalSeasonEvent] = []

    feed_edges = res_json[4]["data"]["explore"]["feed"]["edges"]

    for feed_edge in feed_edges:
        if "group" in feed_edge["node"]:
            group_edges = feed_edge["node"]["group"]["items"]["edges"]
            for group_edge in group_edges:
                model = FestivalSeasonEvent(**group_edge["node"])
                models.append(model)

    return models


def parse_reserved_listings(res_json: List[Dict]) -> TicketswapApiResponseEvent:
    data = {"data": res_json}
    return TicketswapApiResponseEvent(**data)


def parse_structured_event_data(res_json: List[Dict]) -> StructuredEventResponse:
    data = {"data": res_json}
    return StructuredEventResponse(**data)


def parse_events(res_json: List[Dict]) -> Event:
    if res_json:
        if not res_json[0]["data"]["node"]:
            return None
        else:
            return Event(**res_json[0]["data"]["node"])


def drop_duplicates(path: str) -> List[Event]:
    models: List[Event] = []

    with open(path) as f:
        text = f.read()

        if text:
            json_models = json.loads(text)
            for model_json in json_models:
                models.append(Event(**model_json))

    return models
