# Superdesk AAP Changelog

## [1.29.4] Not Released Yet
### Superdesk Change Log
#### Improvements
- [SDESK-4603] Small changes to the IPTC code mappings (#756)

#### Fixes
- (fix): Use hachoir instead of hachoir3 package (#1639)
- [SDESK-4584] In Newsroom, NINJS formatter, HTML links in the body should open in a new browser tab (#753)
- [SDESK-4376] Cursor jumps to line beginning when editing caption/description_text field of Feature Media (#3016)
- [SDESK-4062] Fix scroll in Media Contacts (#3058)
- [SDESK-4571] Do not expire items from production if they reference an assignment (#1643)
- [SDESK-4613] Remove multibyte and characters to avoid from filenames/id's used in Amazon s3 keys (#1647)
- fix(pda parser) Handle unicode chars in input (#755)

### Superdesk Planning Change Log (v1.6.2-rc2)
#### Features
- [SDESK-4469] Introduce modal to prompt for a 'reason' to cancel individual coverages (#1260)
- [SDESK-4427] New Event action 'Mark as Completed' (#1273)

#### Improvements
- [SDESK-3286] Close popup modals with ESC key (#1272)
- [SDESK-4428] Multiselect in the Event list and Planning list (#1268)
- [SDESK-4402] Improve location display in planning lists (#1266)
- [SDESK-4493] Create a history record for Planning items and events when an Event is created from planning item (#1264)
- [SDESK-4421] Add details to location dropdown (#1263)
- [SDBELGA-129] Include coverage without users on export templates (#1281)
- [SDESK-4286] Minor changes to event and planning list items in Export Modal (#1279)
- [SDESK-4566] Position 'start working' as the first item in the action menu for assignments (#1282)
- [SDESK-4573] Slack mentions in slack notifications (#1283)
- [SDESK-4529][SDESK-4534] Show current and future only assignments in the Fulfill modal (#1284)

#### Fixes
- [SDESK-4286] List Item format for exporting and downloading events/planning (#1276)
- [SDESK-4478] Correctly display the number of events in Post/Unpost popup (#1275)
- [SDESK-4549] Coverages are inheriting published time and not scheduled time of a story (#1271)
- [SDESK-4328] Remove ability to clear the coverage type in the editor (1270)
- (fix): Update enzyme-adapter-react-16 (#1269)
- [SDESK-4427] Mark for complete fix to cater for events that start on same day but ahead in time. (#1278)
- [SDESK-4571] Allow content unlinking when content has been archived (1280)
- [SDESK-4552] (fix): Assignment preview not showing from monitoring preview (#1285)
- [SDESK-4477] (fix): Cannot lower repetitions unless on the first event (#1286))
- [SDESK-4511] (fix): Scrollbar required for planning items in CancelEvent modal (#1287)
- [SDESK-4524] Make contact form read only when embedded in read only coverage form (#1289)
- [SDESK-4535] Fulfill assignment available for Reporters (#1288)
- [SDESK-4609] Filter soft deleted locations out from the browse view (#1290)


## [1.29.3-1] 2019-07-24
### Superdesk Change Log
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

