## [1.29.3-1] 2019-07-24
#### Superdesk Change Log
#### Fixed
- [SDESK-4494] (fix): Sync vocab and planning types from production (#748)

## [1.29.3] 2019-07-22
### Superdesk Change Log
#### Added
- [SDESK-4517] Jinja filter to escape quotes and backslashes (#746)
- [SDESK-4503] Formatter for kvh that includes the take key (#745)
- [SDESK-4436] Template for downloading events for courts listing

#### Fixed
- [SDESK-4466] Use default locale for translations if user language is not supported (#1624)
- flake8 version issue and failing places feature (#1625)
- fix(pollution macro) retry requests
- fix(abs macro) upate item when exected on stage macro

### Superdesk Planning Change Log
#### Added
- [SDESK-4063] Add loader animation on file upload
- [SDESK-4400] Time in Event exports are in UTC instead of server timezone
- [SDESK-4329] Show coverage type in palnning widget coverage details
- [SDESK-4307] Locations Management enhancements
- [SDESK-4375] Show 'genre' in assignments list view
- [SDESK-4377] Make ed-note editable in add-to-planning modal
- [SDBELGA-108] Add unused templates at the end of recent event templates list.
- [SDBELGA-108] List all recent event templates is 'limit' query param was not provided.
- [SDBELGA-108] Store event related data as subdict in event templates schema.
- [SDBELGA-108] Event temlates API.
- [SDESK-4368] Publish time in delivery record is not taking content item's publish schedule into account

#### Fixed
- [SDESK-4471] Reschedule and Postpone bugs when editor is open (#1259)
- [SDESK-4453] Round up time when adding coverage for a published/scheduled news item (#1257)
- [SDESK-4435] Cancel-All-Coverage and updating planning form was throwing an etag error (#1258)
- [SDESK-4436] New-line missing in downloaded file (Windows) (#1256)
- [SDESK-4318] Show name in workqueue in absence of slugline and headline (#1255)
- [SDESK-4336] Allow updates to planning items with disabled agendas (#1253)
- [SDESK-4413] Location Popup was closing when location text was selected and mouse click released (#1251)
- (fix) Limit pydocstyle < 4.0
- [SDESK-4453] Coverage schedule time for published or scheduled news item should be derived from the news item
- [SDESK-4451] sequence_no in delivery record was null instead of 0 by default
- [SDESK-4410] Location from an event was not getting deleted
- [SDESK-4410] Bug when setting time for  Coverage Schedule Date
- [SDESK-4414] Locking linked updated news story was locking the assignment

## [0.1] - 2015-09-04

- here be dragons. we start to populate this since now on.

