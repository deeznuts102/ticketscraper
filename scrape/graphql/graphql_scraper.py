from enum import Enum
from typing import Dict, List
import requests  # type: ignore
import json

GRAPHQL_URL = "https://api.ticketswap.com/graphql/public?"

class City(Enum):
    AMSTERDAM = "Q2l0eToz",

class GraphQLScraper:
    def get_popular_events(self, city: City) -> List[str]:
        payload = json.dumps(
            [
                {
                    "operationName": "getPopularEvents",
                    "variables": {
                        "cityId": city.value[0],
                        "period": "ANYTIME",
                        "first": 99,
                        "highlighted": False,
                    },
                    "query": "query getPopularEvents($first: Int, $after: String, $highlighted: Boolean, $period: Period, $dateRange: DateRangeInput, $category: EventCategory, $cityId: ID, $locationId: ID, $nearby: GeopointFilter) {\n  activeEvents(\n    first: $first\n    after: $after\n    period: $period\n    dateRange: $dateRange\n    orderBy: {field: BOOST_VALUE, direction: DESC}\n    filter: {locationId: $locationId, category: $category, highlighted: $highlighted, city: $cityId, nearby: $nearby}\n  ) {\n    period\n    edges {\n      node {\n        ...eventList\n        __typename\n      }\n      __typename\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment eventList on Event {\n  id\n  slug\n  name\n  isHighlighted\n  imageUrl\n  category\n  startDate\n  endDate\n  hasOngoingEventType\n  availableTicketsCount\n  status\n  artists {\n    ...artist\n    __typename\n  }\n  country {\n    ...country\n    __typename\n  }\n  uri {\n    path\n    __typename\n  }\n  location {\n    id\n    name\n    city {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment artist on Artist {\n  id\n  name\n  slug\n  avatar\n  numberOfUpcomingEvents\n  isFollowedByViewer\n  viewerHasNotificationsEnabled\n  __typename\n}\n\nfragment country on Country {\n  name\n  code\n  __typename\n}\n",
                }
            ]
        )

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0",
            "Accept": "*/*",
            "Accept-Language": "en",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.ticketswap.com/",
            "content-type": "application/json",
            "authorization": "",
            "device-id": "df8da00f-0ee0-4776-b3f5-739f7f2c5142",
            "Origin": "https://www.ticketswap.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "TE": "trailers",
        }

        response = requests.request("POST", GRAPHQL_URL, headers=headers, data=payload)

        return json.loads(response.text)

    def get_events_this_weekend(self) -> List[str]:
        payload = json.dumps(
            [
                {
                    "operationName": "getPopularEvents",
                    "variables": {
                        "nearby": {
                            "latitude": 52.2957,
                            "longitude": 6.5832,
                            "radius": 20,
                        },
                        "period": "THIS_WEEKEND",
                        "first": 99,
                    },
                    "query": "query getPopularEvents($first: Int, $after: String, $highlighted: Boolean, $period: Period, $dateRange: DateRangeInput, $category: EventCategory, $cityId: ID, $locationId: ID, $nearby: GeopointFilter) {\n  activeEvents(\n    first: $first\n    after: $after\n    period: $period\n    dateRange: $dateRange\n    orderBy: {field: BOOST_VALUE, direction: DESC}\n    filter: {locationId: $locationId, category: $category, highlighted: $highlighted, city: $cityId, nearby: $nearby}\n  ) {\n    period\n    edges {\n      node {\n        ...eventList\n        __typename\n      }\n      __typename\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment eventList on Event {\n  id\n  slug\n  name\n  isHighlighted\n  imageUrl\n  category\n  startDate\n  endDate\n  availableTicketsCount\n  status\n  artists {\n    ...artist\n    __typename\n  }\n  country {\n    ...country\n    __typename\n  }\n  uri {\n    path\n    __typename\n  }\n  location {\n    id\n    name\n    city {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment artist on Artist {\n  id\n  name\n  slug\n  avatar\n  numberOfUpcomingEvents\n  isFollowedByViewer\n  viewerHasNotificationsEnabled\n  __typename\n}\n\nfragment country on Country {\n  name\n  code\n  __typename\n}\n",
                }
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

    def get_nearby_events(self) -> List[str]:
        payload = json.dumps(
            [
                {
                    "operationName": "nearby",
                    "variables": {"latitude": 52.3647, "longitude": 6.6842},
                    "query": "query nearby($latitude: Float, $longitude: Float) {\n  nearby(latitude: $latitude, longitude: $longitude) {\n    risingEvents(first: 8) {\n      id\n      name\n      startDate\n      imageUrl\n      slug\n      availableTicketsCount\n      location {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    popularLocations(first: 6) {\n      id\n      slug\n      image\n      name\n      background\n      __typename\n    }\n    __typename\n  }\n}\n",
                },
                {
                    "operationName": "getFeedItems",
                    "variables": {"countryCode": "NL"},
                    "query": "query getFeedItems($countryCode: CountryCode) {\n  explore(countryCode: $countryCode) {\n    feed(first: 20) {\n      edges {\n        node {\n          ...thumbnailBlog\n          ...thumbnailEventCollection\n          ...thumbnailWithUrl\n          ...groupCollection\n          ...recurringEventCollection\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment thumbnailBlog on ThumbnailBlog {\n  id\n  type\n  status\n  blogPost {\n    id\n    title\n    subtitle\n    imageUrl\n    body\n    slug\n    author {\n      id\n      firstname\n      __typename\n    }\n    createdAt\n    __typename\n  }\n  __typename\n}\n\nfragment thumbnailEventCollection on ThumbnailEventCollection {\n  id\n  type\n  status\n  title\n  subtitle\n  group {\n    ...group\n    __typename\n  }\n  __typename\n}\n\nfragment group on Group {\n  id\n  subtitle\n  title\n  imageBackgroundUrl\n  imageThumbnailUrl\n  logoUrl\n  items(first: 100) {\n    edges {\n      node {\n        ...eventList\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment eventList on Event {\n  id\n  slug\n  name\n  isHighlighted\n  imageUrl\n  category\n  startDate\n  endDate\n  availableTicketsCount\n  status\n  artists {\n    ...artist\n    __typename\n  }\n  country {\n    ...country\n    __typename\n  }\n  uri {\n    path\n    __typename\n  }\n  location {\n    id\n    name\n    city {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment artist on Artist {\n  id\n  name\n  slug\n  avatar\n  numberOfUpcomingEvents\n  isFollowedByViewer\n  viewerHasNotificationsEnabled\n  __typename\n}\n\nfragment country on Country {\n  name\n  code\n  __typename\n}\n\nfragment thumbnailWithUrl on ThumbnailWithUrl {\n  id\n  type\n  status\n  title\n  subtitle\n  url\n  imageUrl\n  __typename\n}\n\nfragment groupCollection on GroupCollection {\n  id\n  type\n  status\n  title\n  subtitle\n  numberOfItemsOnFeedOverview: numbersOfItemsOnFeedOverview\n  group {\n    ...group\n    __typename\n  }\n  __typename\n}\n\nfragment recurringEventCollection on RecurringEventCollection {\n  id\n  type\n  status\n  title\n  subtitle\n  numberOfEventsOnFeedOverview: numbersOfEventsOnFeedOverview\n  imageBackgroundUrl: imageUrl\n  events {\n    edges {\n      node {\n        ...eventList\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n",
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

    def get_event_structure_data(self, event_id: str) -> List[str]:
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

    def get_reserved_listings(self, event_id: str) -> List[str]:
        payload = json.dumps(
            [
                {
                    "operationName": "getReservedListings",
                    "variables": {"id": f"{event_id}", "first": 10},
                    "query": "query getReservedListings($id: ID!, $first: Int, $after: String) {\n  node(id: $id) {\n    ... on EventType {\n      id\n      slug\n      title\n      reservedListings: listings(\n        first: $first\n        filter: {listingStatus: RESERVED}\n        after: $after\n      ) {\n        ...listings\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment listings on ListingConnection {\n  edges {\n    node {\n      ...listingList\n      __typename\n    }\n    __typename\n  }\n  pageInfo {\n    endCursor\n    hasNextPage\n    __typename\n  }\n  __typename\n}\n\nfragment listingList on PublicListing {\n  id\n  hash\n  description\n  isPublic\n  status\n  dateRange {\n    startDate\n    endDate\n    __typename\n  }\n  uri {\n    path\n    __typename\n  }\n  event {\n    id\n    name\n    startDate\n    endDate\n    slug\n    status\n    location {\n      id\n      name\n      city {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  eventType {\n    id\n    title\n    startDate\n    endDate\n    __typename\n  }\n  seller {\n    id\n    firstname\n    avatar\n    __typename\n  }\n  tickets(first: 99) {\n    edges {\n      node {\n        id\n        status\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  numberOfTicketsInListing\n  numberOfTicketsStillForSale\n  price {\n    originalPrice {\n      ...money\n      __typename\n    }\n    totalPriceWithTransactionFee {\n      ...money\n      __typename\n    }\n    sellerPrice {\n      ...money\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment money on Money {\n  amount\n  currency\n  __typename\n}\n",
                }
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

    def get_sold_listings(self, event_id: str, first: int = 99) -> List[str]:
        payload = json.dumps(
            [
                {
                    "operationName": "getSoldListings",
                    "variables": {"id": event_id, "first": first},
                    "query": "query getSoldListings($id: ID!, $first: Int, $after: String) {\n  node(id: $id) {\n    ... on EventType {\n      id\n      slug\n      title\n      soldListings: listings(first: $first, filter: {listingStatus: SOLD}, after: $after) {\n        ...listings\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment listings on ListingConnection {\n  edges {\n    node {\n      ...listingList\n      __typename\n    }\n    __typename\n  }\n  pageInfo {\n    endCursor\n    hasNextPage\n    __typename\n  }\n  __typename\n}\n\nfragment listingList on PublicListing {\n  id\n  hash\n  description\n  isPublic\n  status\n  dateRange {\n    startDate\n    endDate\n    __typename\n  }\n  uri {\n    path\n    __typename\n  }\n  event {\n    id\n    name\n    startDate\n    endDate\n    slug\n    status\n    location {\n      id\n      name\n      city {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  eventType {\n    id\n    title\n    startDate\n    endDate\n    __typename\n  }\n  seller {\n    id\n    firstname\n    avatar\n    __typename\n  }\n  tickets(first: 99) {\n    edges {\n      node {\n        id\n        status\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  numberOfTicketsInListing\n  numberOfTicketsStillForSale\n  price {\n    originalPrice {\n      ...money\n      __typename\n    }\n    totalPriceWithTransactionFee {\n      ...money\n      __typename\n    }\n    sellerPrice {\n      ...money\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment money on Money {\n  amount\n  currency\n  __typename\n}\n",
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

    def get_available_listings(self, event_id: str, first: int = 99) -> List[str]:
        payload = json.dumps(
            [
                {
                    "operationName": "getAvailableListings",
                    "variables": {"id": event_id, "first": first},
                    "query": "query getAvailableListings($id: ID!, $first: Int, $after: String) {\n  node(id: $id) {\n    ... on EventType {\n      id\n      slug\n      title\n      availableListings: listings(first: $first, filter: {listingStatus: AVAILABLE}, after: $after) {\n        ...listings\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment listings on ListingConnection {\n  edges {\n    node {\n      ...listingList\n      __typename\n    }\n    __typename\n  }\n  pageInfo {\n    endCursor\n    hasNextPage\n    __typename\n  }\n  __typename\n}\n\nfragment listingList on PublicListing {\n  id\n  hash\n  description\n  isPublic\n  status\n  dateRange {\n    startDate\n    endDate\n    __typename\n  }\n  uri {\n    path\n    __typename\n  }\n  event {\n    id\n    name\n    startDate\n    endDate\n    slug\n    status\n    location {\n      id\n      name\n      city {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  eventType {\n    id\n    title\n    startDate\n    endDate\n    __typename\n  }\n  seller {\n    id\n    firstname\n    avatar\n    __typename\n  }\n  tickets(first: 99) {\n    edges {\n      node {\n        id\n        status\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  numberOfTicketsInListing\n  numberOfTicketsStillForSale\n  price {\n    originalPrice {\n      ...money\n      __typename\n    }\n    totalPriceWithTransactionFee {\n      ...money\n      __typename\n    }\n    sellerPrice {\n      ...money\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment money on Money {\n  amount\n  currency\n  __typename\n}\n",
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

    def get_event_data(self, event_id: str) -> List[str]:
        payload = json.dumps(
            [
                {
                    "operationName": "getEventData",
                    "variables": {"id": event_id},
                    "query": "query getEventData($id: ID!) {\n  node(id: $id) {\n    ... on Event {\n      ...event\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment event on Event {\n  ...sharedEventData\n  availableTicketsCount\n  soldTicketsCount\n  ticketAlertsCount\n  cancellationReason\n  isHighlighted\n  tags(first: 1) {\n    edges {\n      node {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  country {\n    code\n    __typename\n  }\n  entranceTypes: types(first: 99, filter: {ticketCategory: ENTRANCE}) {\n    edges {\n      node {\n        ...eventTypeData\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  nonEntranceTypesWithoutGroup: types(\n    first: 99\n    filter: {ticketCategory: NON_ENTRANCE, hasGroup: false}\n  ) {\n    edges {\n      node {\n        ...eventTypeData\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  eventTypeGroups {\n    id\n    name\n    eventTypes {\n      ...eventTypeData\n      __typename\n    }\n    __typename\n  }\n  redirectedTo {\n    id\n    slug\n    __typename\n  }\n  availableListings: listings(first: 2, filter: {listingStatus: AVAILABLE}) {\n    edges {\n      node {\n        id\n        price {\n          originalPrice {\n            ...money\n            __typename\n          }\n          __typename\n        }\n        seller {\n          id\n          avatar\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  soldListings: listings(first: 2, filter: {listingStatus: SOLD}) {\n    edges {\n      node {\n        id\n        seller {\n          id\n          avatar\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  externalPrimaryTicketShops {\n    ...externalPrimaryTicketShop\n    __typename\n  }\n  __typename\n}\n\nfragment sharedEventData on Event {\n  id\n  slug\n  name\n  status\n  isEventFavoritedByUser\n  isSellingBlocked\n  isBuyingBlocked\n  isPopular\n  category\n  timeZone\n  instagramUsername\n  startDate\n  endDate\n  hasOngoingEventType\n  tags(first: 1) {\n    edges {\n      node {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  facebookEventWalls {\n    facebookUrl\n    isMainEventWall\n    __typename\n  }\n  isVerified\n  seoMetadata {\n    title\n    description\n    __typename\n  }\n  description\n  eventVideo {\n    ...eventVideo\n    __typename\n  }\n  closedLoopInformation {\n    ...closedLoopInformation\n    __typename\n  }\n  secureSwapInformation {\n    isManualSecureSwapAvailable\n    __typename\n  }\n  alias {\n    uri {\n      url\n      path\n      __typename\n    }\n    __typename\n  }\n  headerImageUrl\n  imageUrl\n  imageSmallUrl\n  organizerShop {\n    id\n    organizerBranding {\n      name\n      image\n      __typename\n    }\n    hasDynamicProducts\n    __typename\n  }\n  location {\n    id\n    slug\n    name\n    geoInfo {\n      latitude\n      longitude\n      __typename\n    }\n    background\n    amountOfActiveUpcomingEvents\n    image\n    website\n    averageFanExperienceRating\n    totalAmountOfFanExperiences\n    city {\n      id\n      slug\n      name\n      __typename\n    }\n    country {\n      ...country\n      __typename\n    }\n    __typename\n  }\n  organizerBrands {\n    ...organizerBrand\n    __typename\n  }\n  artists {\n    ...artist\n    __typename\n  }\n  types(first: 99) {\n    edges {\n      node {\n        id\n        slug\n        title\n        availableTicketsCount\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  warning {\n    title\n    message\n    url {\n      text\n      url\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment artist on Artist {\n  id\n  name\n  slug\n  avatar\n  numberOfUpcomingEvents\n  isFollowedByViewer\n  viewerHasNotificationsEnabled\n  __typename\n}\n\nfragment organizerBrand on OrganizerBrand {\n  id\n  name\n  logoUrl\n  isFollowedByViewer\n  displayRequestForMarketingConsent\n  __typename\n}\n\nfragment eventVideo on EventVideo {\n  id\n  platform\n  videoPlatformId\n  videoUrl\n  title\n  thumbnailUrl\n  __typename\n}\n\nfragment closedLoopInformation on ClosedLoopEventInformation {\n  ticketProviderName\n  findYourTicketsUrl\n  __typename\n}\n\nfragment country on Country {\n  name\n  code\n  __typename\n}\n\nfragment eventTypeData on EventType {\n  id\n  slug\n  title\n  startDate\n  endDate\n  isOngoing\n  availableTicketsCount\n  isOngoing\n  isSellingBlocked\n  __typename\n}\n\nfragment externalPrimaryTicketShop on ExternalPrimaryTicketShop {\n  id\n  startDate\n  state\n  shopImageUrl {\n    url\n    trackingUrl\n    path\n    host\n    __typename\n  }\n  shopUrl {\n    url\n    trackingUrl\n    path\n    host\n    __typename\n  }\n  __typename\n}\n\nfragment money on Money {\n  amount\n  currency\n  __typename\n}\n",
                }
            ]
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0",
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
