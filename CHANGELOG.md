# Superdesk AAP Changelog

## [1.30] Not Released Yet
### AAP-Superdesk Change Log
#### Features
- None

#### Improvements
- [SDESK-3946] Enable table chart for SMS Report (#761)
- [SDESK-4660] Worldview macro (#766)

#### Fixes
- (fix): editFeaturedImage setting should use boolean not int (#760)
- [SDESK-4619] (fix): MissionReport limiting kills/takedowns/correction results (#763)
- (fix-requirements) Add responses to dev-requirements.txt (#768)
- fix(abs macro) stop null values crashing the macro (#765)
- Add AP to AAP anpa category map (#767)
- fix world view to handle empty subject codes (#771)

### Superdesk-Core Change Log (v1.30.1)
#### Feature
- [SDESK-3834] setup `extract_messages` command (superdesk-core#1574)
- [SDESK-4395] AP Media API Implimentation (superdesk-core#1619)

#### Improvements
- [SDANSA-196] add shortcut flag to saved searches (superdesk-core#1577)
- [SDNTB-577] add item_publish signal (superdesk-core#577)
- Provide an additional request arguments for download_file_from_url function (superdesk-core#1592)
- [SDESK-4272] Additional logging in expiry (superdesk-core#1594)
- [SDESK-2390] add structured field info to publish validation errors (superdesk-core#1597)
- [SDANSA-269] log time for media upload (superdesk-core#1605)
- [SDESK-4649] Additional Filter Condition operators for place (superdesk-core#1651)

### Fixes
- Fix AttributeError when url is not in config. Remove redundant validation (superdesk-core#1581)
- [SDESK-4105] fix(upload): make media description multi line field (superdesk-core#1583)
- [STTNHUB-58] - Auto published ingested items should preserve id (superdesk-core#1579)
- [SDANSA-267] avoid validation errors for missing cvs (superdesk-core#1590)
- [SDESK-4150] (validation) fix subject required error when custom vocabulary is used (superdesk-core#1593)
- handle application/ content type reponses when fetching image from url (superdesk-core#1599)
- [SDESK-4129] Fixed: Cannot deschedule scheduled articles (superdesk-core#1578)
- [SDESK-4229] fixed: fetched image item belonging to package can't be saved in media gallery (superdesk-core#1591)
- [SDANSA-266] fix(formatter): fix newsmlg2 sent timestamp was wrong (superdesk-core#1606)
- [SDANSA-252] avoid client caching when fetching content profile for editing (superdesk-core#1604)
- fix newsml g2 content parser and introduce new item_validate signal (superdesk-core#1621)
- [SDESK-4466] (fix): Use default locale for translations if user language is not supported (superdesk-core#1623)
- [SDESK-4423][SDESK-4463] Fix ordering of media-gallry and related items in ninjs (superdesk-core#1632)
- [SDESK-4463] fix ordering of related items in ninjs output (superdesk-core#1640)
- [SDESK-4574] fix related items reference in associations (superdesk-core#1641)
- [SDESK-4004] fix 'Edit image' action done from article should not modify the original image file (superdesk-core#1620)
- fix(ap category mapping) Numbers in sluglines failed to parse and fix mapping (superdesk-core#1662)
- fix(flake8): Resolve 'D413 Missing blank line after last section' (superdesk-core#1669)
- fix(pymongo): set pymongo version to 3.8 (some issues with 3.9) (superdesk-core#1666)
- (fix-1.30) flake8 version issue and failing places feature (superdesk-core#1625)

### Superdesk-Client-Core Change Log (v1.30.4)
#### Feature
- Settings Dashboard (superdesk-client-core#2926)
- [SDESK-4128] FunctionPoint service for generic function extensions (superdesk-client-core#2930)
- [SDANSA-196] feat(search): display selected saved searches as shortcuts (superdesk-client-core#2925)
- [SDANSA-247] add initial middleware support to authoring (superdesk-client-core#2948)
- [SDESK-4262] fetch images from external source when dropped to editor3 (superdesk-client-core#2961)

#### Improvements
- remove-old-errors-after-successful-save (superdesk-client-core#2934)
- [SDESK-4179] Add instagram icon to contact info card in Media Contacts page (superdesk-client-core#2938)
- [SDESK-4122] Allow assignment notification to open the assignment on clicking (superdesk-client-core#2939)
- [SDESK-4129] Make delaying of item creation in internal destinations configurable. (superdesk-client-core#2965)
- [SDANSA-297] implement line count component (superdesk-client-core#3007)
- [SDESK-4274] Small move of the public switch in the contacts form (superdesk-client-core#3012)

#### Fixes
- [SDESK-4112] Text added before or after an annotation does not activate the save button and throws errors in console (superdesk-client-core#2916)
- [SDESK-4107] Fixed(Custom CVs): 'Single selection' option is not reflected in the editor. (superdesk-client-core#2918)
- [SDESK-4182] fixed: can't save changes in saved search (superdesk-client-core#2931)
- [SDESK-2393] Remove the publish button when an item in personal is selected (superdesk-client-core#2933)
- [SDESK-2390] fix(authoring): add missing error indicator on custom required fields (superdesk-client-core#2940)
- [SDESK-4175][SDESK-4187] (editor-3) Image dropped next to table area crashes the editor (superdesk-client-core#2941)
- [SDESK-4203] Hide 'edit in new window' button if the item is locked by current user (superdesk-client-core#2944)
- [SDESK-4158] Fixed: Pasted metadata is lost if image is deselected & then selected again. (superdesk-client-core#2936)
- [SDESK-4226] Fixed: When editing routed composite an item's view stretches the image displayed to an enormously large scale (superdesk-client-core#2946)
- [SDESK-4255] Prohibit drag and drop of saved authoring item or ingested composite items to featured media field (superdesk-client-core#2947)
- [SDESK-4201] fixed: Broken media gallery (superdesk-client-core#2943)
- (fix): FunctionPoint 'authoring:publish' not sending through _id and type (superdesk-client-core#2949)
- [SDESK-4183] fix(search): Fix issue saving changes on search after updating subscriptions (superdesk-client-core#2935)
- [SDESK-4265] Hide copy/paste metadata button from 'edit image' section (superdesk-client-core#2954)
- [SDESK-4257] Fix(Subscribers): Cannot create 'Content API-only' destination (superdesk-client-core#2953)
- [SDANSA-261] Bug the counter of max chars for body html does not work (superdesk-client-core#2956)
- fix(editor3): fix typo in generated html (superdesk-client-core#2963)
- fix(authoring): make fetched image from external source editable (superdesk-client-core#2968)
- add: publishing side panel class for Publisher SEO UI implementation (superdesk-client-core#2971)
- [SDESK-4182] fixed: While editing saved searches some of the fields do not keep and display the search criteria that was originally there. (superdesk-client-core#2942)
- fix default edit featured image config (superdesk-client-core#2973)
- [SDESK-4237] Set 'Allow multiple items' limit in related content to minimum 2. (superdesk-client-core#2945)
- [SDESK-3380] Fixed: error is thrown on sending correction for an item containing images with adjusted brightness in custom media field (superdesk-client-core#2962)
- [SDANSA-265] As a user i don t have a use for the td button in the editor toolbar (superdesk-client-core#2958)
- [SDESK-2390] fix error display in authoring for custom fields (superdesk-client-core#2964)
- [SDESK-4310][SDESK-4333] Fix embeds in preview (superdesk-client-core#2982)
- [SDANSA-273] fix(monitoring): Fixed issue with infinite scroll on single stage (superdesk-client-core#2984)
- [SDBELGA-105] (media-metadata-editor): Fixed support for custom text fields as metadata. (superdesk-client-core#2972)
- [SDESK-4194] fix: Changes in subscribers content API tab are not activating the save button (superdesk-client-core#2979)
- [SDESK-4303] fixed: Removing a filter statement from a content filter does not enable the save button. (superdesk-client-core#2981)
- Fix support for string fields (superdesk-client-core#2991)
- [SDANSA-282] Fix duplicated string fields (like language) on image upload (superdesk-client-core#2998)
- [SDESK-4412] Content views are not getting more items on scroll (superdesk-client-core#3001)
- fix(metadata): Fixed issue with list scroll on metadata widget (superdesk-client-core#3010)
- [SDANSA-282] Fix photo upload form (superdesk-client-core#3002)
- [SDANSA-307][SDANSA-308] fix search shortcuts (superdesk-client-core#3032)
- [SDESK-4496] fix(poi):: Fixed issue with setting default poi (superdesk-client-core#3044)
- [SDESK-4574] fix related item references including full item for published items (superdesk-client-core#3048)
- [SDESK-4004] Fixed: 'Edit image' action done from article should not modify the orginial image file. (superdesk-client-core#3011)
- [SDESK-4658] Fix grammar issue with default ednote for a correction (superdesk-client-core#3082)
- backward compatibility fix

### Superdesk Planning Change Log (v1.7.0-rc2)
#### Features
- [SDESK-4427] New Event action 'Mark as Completed' (#1273)
- [SDNTB-584] feat(draggable): Added ability to make modals draggable (#1294)

#### Improvements
- [SDESK-4599] Review planning workflow notifications (#1301)
- [SDESK-4598] Add Place to event and planning filter (#1302)
- [SDESK-4618] Remove the folder from the filename returned for attachments (#1307)
- [SDESK-4595] Move the attachment icon in lists (#1311)
- [SDESK-4651] Show all desks by default in Fulfil Assignment modal (#1305)
- [SDESK-4676] Hide 'all day' as an event form option (#1320)

#### Fixes
- [SDESK-4427] Mark for complete fix to cater for events that start on same day but ahead in time. (#1278)
- [SDESK-4592] Restrict some item actions on expired items (#1297)
- actioned_date was removed when posting an event (#1299)
- [SDESK-4224][SDESK-4510][SDESK-4513] (fix): Don't unmount the PopupEditor when action modal is shown (#1274)
- [SDESK-4572] Don't close dropdown on scroll bar click (#1303)
- [SDESK-4654] Handle the enter key in Selecting subject codes etc. (#1312)
- [SDESK-4669] Location was getting deleted when event was marked as complete or assigned to calendar (#1310)
- [SDESK-4661] (fix) Fulfil Assignment button visible if Assignment is locked (#1306)
- (fix-requirements) Add responses lib in dev-requirements.txt (#1315)
- [SDESK-4678] When marking an Event as completed Planning and Assignments need to be updated (#1317)
- fix(flake8): Resolve 'D413 Missing blank line after last section' (#1312)
- fix(import ui-framework): Add helpers and colors to scss imports (#1323)
- fix to use modal__backdrop class locally (#1326)
- [SDESK-4691] Planning was not published when event was completed (#1330)


## [1.29.4] 2019-08-21
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
- [SDESK-4641] (fix): Item not being removed from workqueue on publish (#3067)
- [SDESK-4634] (fix): Update newsroom formatter to use abstract not alt_text
- fix(ap anpa wordcount) Handle missing word count (#1649)

### Superdesk Planning Change Log (v1.6.2)
#### Features
- [SDESK-4469] Introduce modal to prompt for a 'reason' to cancel individual coverages (#1260)

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
- [SDESK-4571] Allow content unlinking when content has been archived (1280)
- [SDESK-4552] (fix): Assignment preview not showing from monitoring preview (#1285)
- [SDESK-4477] (fix): Cannot lower repetitions unless on the first event (#1286))
- [SDESK-4511] (fix): Scrollbar required for planning items in CancelEvent modal (#1287)
- [SDESK-4524] Make contact form read only when embedded in read only coverage form (#1289)
- [SDESK-4535] Fulfill assignment available for Reporters (#1288)
- [SDESK-4609] Filter soft deleted locations out from the browse view (#1290)
- [SDESK-4637] (fix) Select first assignment on fulfill on publish (#1296)
- [SDESK-4608] (fix) Advance Search Panel was collapsing if list item has a long text (#1298)


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

