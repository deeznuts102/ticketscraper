# ticketscraper

[Latest files]()

## Using datamodel-code-generator to generate models from JSON

1. Download JSON file locally e.g. as `result.json`
2. Run `datamodel-code-generator` module to generate models:

```bash
datamodel-codegen --input result.json --input-file-type json --output models/res.py --class-name Event  --snake-case-field   --use-schema-description --use-title-as-name --target-python-version 3.9
```

---

Entity Nearby:
https://api.ticketswap.com/graphql/public?getPopularEvents

input:
nearby: {
    latitutde:
    longitude:
    radius
}
period: THIS_WEEKEND
first: 50

output:
slug: {2}->data->activeEvents->edges->0->node->uri->path
eventId: {2}->data->activeEvents->edges->0->node->uri->path
location_name: {2}>data>activeEvents>edges[0]->node->location->name
city_name: {2}>data>activeEvents>edges[0]->node->location->city->name

---

Entity EntranceTypes:
https://www.ticketswap.com/_next/data/3611f8970f57d0a4a0d826e114365d9afa9faa93/en/event/avonturenpark-hellendoorn/7b3addf1-9edb-4ba9-adfe-fd625c1fac4d.json?eventSlug=avonturenpark-hellendoorn&eventIdOrEventTypeSlug=7b3addf1-9edb-4ba9-adfe-fd625c1fac4d

input:
id: 3611f8970f57d0a4a0d826e114365d9afa9faa93 -> main page element in HTML document
slug: avonturenpark-hellendoorn
eventid: 7b3addf1-9edb-4ba9-adfe-fd625c1fac4d

output:
event_slug: pageProps->event>entranceTypes>edges>0>node>slug
availableTicketsCount: pageProps->event->availableTicketsCount 
soldTicketsCount: pageProps->event->soldTicketsCount 
ticketAlertsCount: pageProps->event->ticketAlertsCount 
startDate: pageProps->event->startDate
endDate: pageProps->event->endDate
entrance_type_slug: pageProps->event->EntranceTypes->slug

---

Entity tickets:
https://www.ticketswap.com/_next/data/3611f8970f57d0a4a0d826e114365d9afa9faa93/en/event/avonturenpark-hellendoorn/flex-entreeticket/7b3addf1-9edb-4ba9-adfe-fd625c1fac4d/2243185.json?eventSlug=avonturenpark-hellendoorn&eventId=7b3addf1-9edb-4ba9-adfe-fd625c1fac4d&eventIdOrEventTypeSlug=flex-entreeticket&eventTypeId=2243185

input:
id: Same as before
event_slug: same
subevent_slug: flex-entreeticket
eventId: same
optional: event_type_id" 2243185


output:
startDate:pageProps>initalApolloState>EventType:<eventTypeId>->startDate
endDate:pageProps>initalApolloState>EventType:<eventTypeId>->endDate
originalPrice: pageProps>initialApolloState>PublicListing>Price>originalPrice
totalPriceWithTransactionFee: pageProps>initialApolloState>PublicListing>Price>originalPrice
sellerPrice: pageProps>initialApolloState>PublicListing>Price>sellerPrice
numberOfTicketsStillForSale: pageProps>initialApolloState>PublicListing>Price>numberOfTicketsStillForSale




