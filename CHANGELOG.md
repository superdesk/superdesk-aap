# Superdesk AAP Changelog

## [1.31.0] 2020-03-03
### AAP-Superdesk Changelog
- [SWP-1525] - Setting the default category per environment variable (#700)
- [SDESK-4864] Macro to process incoming acceptance email (#829)
- [SDESK-5072] Enable config option PLANNING_USE_XMP_FOR_PIC_SLUGLINE (#830)

## Superdesk-Core Change Log (v1.31.6)
#### Features
- Mark For User:
  - [SDBELGA-124] As a user I want to be notified when a story is marked for me. (superdesk/superdesk-core#1634)
  - Add mark for user to available metadata fields (superdesk/superdesk-core#1617)
- Unpublish Content:
  - [SDFID-555] implement unpublish feature (superdesk/superdesk-core#1629)
  - [SDFID-573] set custom validation error message for unpublishing (superdesk/superdesk-core#1663)

#### Improvements
- [SDESK-4589] Add Mongo indexes to items/items_versions to speed up the expiry command (superdesk/superdesk-core#1644)
- [SDFID-569] [FORMATTER][NINJS] Added `code` to authors (superdesk/superdesk-core#1648)
- setup: updated celery minimal version to 4.3.0 (superdesk/superdesk-core#1587)
- [SDNTB-594] implement high priority queue for subscriber transmission (superdesk/superdesk-core#1645)
- [SDANSA-312] add sent desk output type for monitoring (superdesk/superdesk-core#1642)
- [SDFID-555] return related items for given item (superdesk/superdesk-core#1636)
- [SDBELGA-132] [SPELLCHECKERS] default spellchecker implementation + discard spelling mistakes (superdesk/superdesk-core#1626)
- [SWP-1525] Setting the default category per environment variable (superdesk/superdesk-core#1582)
- introduce `item_validate` signal for custom validation (superdesk/superdesk-core#1621)
- [SDBELGA-122] [SPELLCHECKERS] implemented Leuven University Dutch Spellchecker (superdesk/superdesk-core#1618)
- [SDBELGA-86] add custom_field_type field to vocabulary (superdesk/superdesk-core#1602)
- [SDBELGA-109] [SPELLCHECKERS] Spellcheckers integration + Grammelecte implemention (superdesk/superdesk-core#1601)

#### Fixes
- [SDESK-4652] (fix): Redis client fails to connect using amqp scheme (superdesk/superdesk-core#1652)
- [SDESK-4742] Generate custom renditions on image upload by default. (superdesk/superdesk-core#1690)
- make sure we don't send multiline email subjects (superdesk/superdesk-core#1667)
- fix ninjs not generated properly when rendition is empty (superdesk/superdesk-core#1661)
- avoid recursive ninjs formatting for related items (superdesk/superdesk-core#1658)
- [SDESK-4491] return crop data for original rendition size on media operation (superdesk/superdesk-core#1655)
- fix data update for related items (superdesk/superdesk-core#1654)
- fix unstable e2e tests (superdesk/superdesk-core#1650)
- [SDESK-4606] fix renditions generated during ingest not using crop (superdesk/superdesk-core#1646)
- [SDESK-4497] fix wrong prepopulate data (superdesk/superdesk-core#1637)
- [SDANSA-309] [SDANSA-307] fix saved search report not using doc_type (superdesk/superdesk-core#1635)
- [SDESK-4531] there should be no format options set for headline (superdesk/superdesk-core#1638)
- use custom subjects for names when parsing newsml (superdesk/superdesk-core#1628)
- [SDANSA-307] [SDANSA-309] fix saved search reports (superdesk/superdesk-core#1633)
- [SDESK-4372] [FEEDING SERVICES][AP] only get last 25 items when provider is new or reopened (superdesk/superdesk-core#1631)
- Fix(tests) Remove 'assert_200' from put step. (superdesk/superdesk-core#1609)
- [SDESK-4466] (fix): Use default locale for translations if user language is not supported (superdesk/superdesk-core#1623)
- fix validation with custom type (superdesk/superdesk-core#1627)
- fix ansa culture ingest content parsing (superdesk/superdesk-core#1621)
- fix flake8 after lib update (superdesk/superdesk-core#1622)
- Fixed typo in comments for http_push service (superdesk/superdesk-core#1613)
- [SDESK-4397] [FEATURES] fixed places.feature (superdesk/superdesk-core#1616)
- [SDESK-4397] [FEATURES] fixed places.features (superdesk/superdesk-core#1615)
- [SDESK-4200] concept items: implicitly apply case insensitive collation for name and definition fields. (superdesk/superdesk-core#1600)
- [SDANSA-252] avoid client caching when fetching content profile for editing (superdesk/superdesk-core#1604)
- Add readonly flag to resource relation helper. (superdesk/superdesk-core#1603)

## Superdesk-Client-Core Change Log (v1.31.3)
#### Features
- Unpublish Content:
	- [SDFID-573] add error/success notifications for unpublish actions (superdesk/superdesk-client-core#3091)
	- [SDFID-555] add unpublish action for published content (superdesk/superdesk-client-core#3024)
- Mark For User
	- [SDBELGA-123] refresh the list when items are marked/unmarked for user (superdesk/superdesk-client-core#3055)
	- [SDBELGA-123] List content marked for me (superdesk/superdesk-client-core#3018)
	- [SDBELGA-29] Mark for user  display people content is marked for (superdesk/superdesk-client-core#2997)
	- [SDBELGA-28] Mark for user (superdesk/superdesk-client-core#2989)
- [SDESK-4261] Client side extensions (superdesk/superdesk-client-core#2950)

#### Improvements
- [SDESK-4983] Make items with pubstatus withheld unfetchable (superdesk/superdesk-client-core#3324)
- [SDESK-4861] Migrate functionPoints to extensions API (superdesk/superdesk-client-core#3301)
- [SDANSA-318] add extension point for iptc mapping (superdesk/superdesk-client-core#3069)
- [SDNTB-593] As a user I want to see scheduled date and time for the items in the 'scheduled output' stage. (superdesk/superdesk-client-core#3059)
- Search bar improvements (superdesk/superdesk-client-core#3060)
- [SDBELGA-132] enable add to dictionary for external spellcheckers (superdesk/superdesk-client-core#3062)
- [SDNTB-594] add priority switch to subscribers (superdesk/superdesk-client-core#3057)
- [SDANSA-270] Add buttons for adding features and gallery photos (superdesk/superdesk-client-core#3052)
- [SDANSA-312] add desk sent output group to monitoring (superdesk/superdesk-client-core#3049)
- [SDANSA-304] Add uppercase and lowercase buttons to editor3 (superdesk/superdesk-client-core#3033)
- [SDESK-4325] Save changes made to desk if user agrees by clicking save on confirmation prompt. (superdesk/superdesk-client-core#3040)
- [SDBELGA-113] Show message for style suggestions in the spellchecker (superdesk/superdesk-client-core#3042)
- [SDFID-562] improve list performance (superdesk/superdesk-client-core#3039)
- [SDESK-1299] feat(selectAll): Added select all functionality for user privileges (superdesk/superdesk-client-core#3025)
- [SDESK-4384] Add edit crops screen after image upload to body field. (superdesk/superdesk-client-core#3014)
- Grammalecte & Leuven spellcheckers (superdesk/superdesk-client-core#2976)
- [SDESK-4274] Small move of the public switch in the contacts form (superdesk/superdesk-client-core#3012)
- [SDBELGA-86] add api for custom field types (superdesk/superdesk-client-core#2975)
- [SDESK-4012] Enable custom video and audio as well as related items to show up in the preview. (superdesk/superdesk-client-core#3005)
- [SDANSA-297] implement line count component (superdesk/superdesk-client-core#3007)
- [SDNTB-545] Add default option to custom sort of groups (superdesk/superdesk-client-core#2994)
- Create planning extension (superdesk/superdesk-client-core#2974)
- [SDNTB-545] feat(monitoring): Custom sort for a single/multiple group in monitoring (superdesk/superdesk-client-core#2980)
- [SDBELGA-109] Improve spellchecker interface (superdesk/superdesk-client-core#2951)
- Annotations library extension (superdesk/superdesk-client-core#2966)
- [SDBELGA-88] As a user i want to use different spell checkers for different languages (superdesk/superdesk-client-core#2932)

#### Fixes
- [SDESK-4719] No left margin in User profile -> Personal preferences (superdesk/superdesk-client-core#3124)
- [SDESK-4697] fix fetch all (superdesk/superdesk-client-core#3330)
- [SDESK-4697] fetch all internal destinations (superdesk/superdesk-client-core#3283)
- use older chromedriver version (superdesk/superdesk-client-core#3116)
- [SDANSA-321] display string fields with no cv (superdesk/superdesk-client-core#3103)
- [SDANSA-318] fix image upload for picture without iptc metadata (superdesk/superdesk-client-core#3078)
- [SDESK-4621] Fixed: Media carousel breaks once the order of the items is changed. (superdesk/superdesk-client-core#3068)
- [SDESK-4635] Bottom part of small preview is not completely visible (superdesk/superdesk-client-core#3072)
- [SDESK-4615] UI issue with 'not for publication' label in list view (superdesk/superdesk-client-core#3072)
- [SDESK-4576] fix(monitoring): Fixed missing dates on monitoring view (superdesk/superdesk-client-core#3073)
- [SDFID-568] fixed: Annotations library stopped loading fully after a link was added. (superdesk/superdesk-client-core#3070)
- [SDESK-4583] Fixed: save button is inactive after uppercase/lowercase operation. (superdesk/superdesk-client-core#3066)
- [SDESK-4491] when crop modal is opened it shouldn't ask for save/cancel (superdesk/superdesk-client-core#3063)
- [SDANSA-317] fix setting language in media metadata modal (superdesk/superdesk-client-core#3064)
- fix e2e tests (superdesk/superdesk-client-core#3065)
- [SDESK-4606] fix cropping not respecting crop size (superdesk/superdesk-client-core#3061)
- [SDESK-4596] fix: Media gallery stops functioning properly when adding the last item before limit is reached. (superdesk/superdesk-client-core#3053)
- [SDESK-4297] Fix: Drag and drop of media to body editor 3 from external folder is not working. (superdesk/superdesk-client-core#3054)
- Update UI framework version (superdesk/superdesk-client-core#3047)
- Fixes and improvements for crud manager and generic list (superdesk/superdesk-client-core#3029)
- [SDESK-4539] Fixed: on typing something in the caption of media gallery cursor is lost and blinking is observed. (superdesk/superdesk-client-core#3050)
- [SDESK-2390] fix errors not highlighted in authoring for custom fields (superdesk/superdesk-client-core#3043)
- [SDESK-4405] Spellchecker should respond to language change immediately. (superdesk/superdesk-client-core#3027)
- [SDESK-4533] Articles with long headlines should show limited in the list display (superdesk/superdesk-client-core#3045)
- (fix): Postinstall requires css packages (superdesk/superdesk-client-core#3046)
- [SDANSA-307] [SDANSA-308] fix search shortcuts (superdesk/superdesk-client-core#3032)
- use upgraded react in ui-framework (superdesk/superdesk-client-core#3038)
- upgrade react (superdesk/superdesk-client-core#3034)
- [SDESK-4420] Fixed issue with coping and pasting metadata (superdesk/superdesk-client-core#3035)
- [SDANSA-282] Fix photo upload form (superdesk/superdesk-client-core#3026)
- [SDESK-4486] Alignment issue when superscript is used in ordered list (superdesk/superdesk-client-core#3030)
- [SDESK-4500] Change stage name color to more visible one (superdesk/superdesk-client-core#3030)
- [SDESK-4325] Issues with saving changes in the Desk settings. (superdesk/superdesk-client-core#3000)
- [SDESK-3885] Force selection when closing popup on editor3 (superdesk/superdesk-client-core#3028)
- [SDESK-2300] fix(publish): Fixed issue with no-messages on multi publish button (superdesk/superdesk-client-core#3019)
- [SDESK-4376] Cursor jumps to line beginning when editing caption/description_text field of Feature Media (superdesk/superdesk-client-core#3016)
- [SDESK-4335] Avoid extending inline styles when pressing space at end of block (superdesk/superdesk-client-core#3013)
- [SDESK-4408] Fixed: Unlocking items from preview does not work if the item is open in authoring. (superdesk/superdesk-client-core#3023)
- [SDESK-4458] Save button does not stay on top when scrolling down in multi-edit (superdesk/superdesk-client-core#3022)
- [SDESK-4457] Minor UI issue in multi-edit (superdesk/superdesk-client-core#3022)
- don't allow returning empty values from prompt (superdesk/superdesk-client-core#3020)
- fix(postinstall): Only compile e2e tests if protractor is installed (superdesk/superdesk-client-core#3021)
- fix(postinstall): Compile e2e requires protractor installed (superdesk/superdesk-client-core#3017)
- compile e2e tests post install. grunt task doesn't work in parent repositories (superdesk/superdesk-client-core#3015)
- Port e2e tests to TypeScript (superdesk/superdesk-client-core#3004)
- fix(metadata): Fixed issue with list scroll on metadata widget (superdesk/superdesk-client-core#3010)
- [SDBELGA-105] Fixed: Can't enter values for custom text fields on image upload. (superdesk/superdesk-client-core#3009)
- [SDESK-4391] Fix: Multi-edit is not displaying any of the items fields. (superdesk/superdesk-client-core#3008)
- Update UI framework (superdesk/superdesk-client-core#3006)
- [SDESK-4388] fix(CP): Fixed content profile missing button (superdesk/superdesk-client-core#2993)
- [SDESK-4386] Fixed: Cannot insert embeds to body. (superdesk/superdesk-client-core#2996)
- [SDESK-4347] Firefox: Edit metadata of an image in the article - broken design (superdesk/superdesk-client-core#2995)
- UI framework update (superdesk/superdesk-client-core#2992)
- [SDBELGA-120] Fix parser when html had empty characters (superdesk/superdesk-client-core#2990)
- [SDESK-4333] Make embeds responsive (superdesk/superdesk-client-core#2987)
- [SDESK-4337] fix: creating a template - the language and custom vocabulary fields have some reserved characters. (superdesk/superdesk-client-core#2985)
- [SDESK-4322] fix: disallow multiple media items -> Save button does not get enabled afterwards. (superdesk/superdesk-client-core#2988)
- [SDESK-4308] fix: Links from preview lead to a blank page. (superdesk/superdesk-client-core#2983)
- [SDESK-4283] Change colours used in suggestion mode to make them visible for colour-blind people (superdesk/superdesk-client-core#2986)
- [SDESK-4310] [SDESK-4313] Embed and style fixes (superdesk/superdesk-client-core#2978)
- [SDESK 4298] Editing annotation results in loss of text field and errors in console (superdesk/superdesk-client-core#2970)
- Build extensions from client repositories (superdesk/superdesk-client-core#2977)
- [SDESK-4237] Set 'Allow multiple items' limit in related content to minimum 2. (superdesk/superdesk-client-core#2945)
- [SDESK-4182] fixed: While editing saved searches some of the fields do not keep and display the search criteria that was originally there. (superdesk/superdesk-client-core#2942)
- Install extensions via npm script (superdesk/superdesk-client-core#2967)
- [SDESK-4251] Refactor the article side-tab widgets and consolidate the list views in them (superdesk/superdesk-client-core#2955)
- Fix end to end test (superdesk/superdesk-client-core#2957)

### Superdesk Planning Change Log (v1.11.0-rc1)
#### Features
- None

#### Improvements
- Update minimum Superdesk to version 1.31
- [SDESK-4989] Add an [X] button to remove selected items from the Download/Export modal in Planning (superdesk/superdesk-planning#1442)
- [SDESK-4864] Add accepted flag (superdesk/superdesk-planning#1441)
- [SDESK-5006] Expandable textarea input for internal_note (superdesk/superdesk-planning#1443)
- [SDESK-5072] Derive coverage slugline from XMP for photo coverages (superdesk/superdesk-planning#1448)

#### Fixes
- [SDESK-4861] Remove usage of functionPoints (superdesk/superdesk-planning#1411)
- [SDESK-5068] Sanitize Input data when saving event/planning (superdesk/superdesk-planning#1438)
- [SDESK-4941] Unposting planing item with assignment was removing planning editor lock (superdesk/superdesk-planning#1439)
- [SDESK-4988] Cannot save/update completed events (superdesk/superdesk-planning#1440)
- [SDESK-5071] Creating planing from killed events (superdesk/superdesk-planning#1445)
- [SDESK-4852] Limit calendar and agenda display in lists (superdesk/superdesk-planning#1444)
- [SDESK-5020] FIX: Issues with advance coverage mode (superdesk/superdesk-planning#1446)
- fix(behave): Add privilege error message in expected response (superdesk/superdesk-planning#1435)

### Superdesk Analytics Change Log (v1.7.4)
- fix(build): Use github/commit for highcharts export server version (superdesk/superdesk-analytics#118)

## [1.30.6] 2020-03-02
### AAP-Superdesk Changelog
- fix(golf macro) missing region and sort order (#822)
- fix(racing macro) set the genre in the selections based on the genre of the original article (#823)

## [1.30.5] 2020-02-25
### AAP-Superdesk Changelog
- [SDESK-5010] Update pictures assignments in progress in DC (#821)
- [SDESK-4863] Implement an Assignment Email layout that allows 'acceptance' of assignments (#825)
- [SDESK-5023] Use display name 'NBA' for iptc subject code 15008001 (#826)

### Superdesk-Core Change Log (v1.30.1)
- [SDESK-5021] Extend FTP transmit to push associations (superdesk/superdesk-core#1809)

### Superdesk-Client-Core Change Log (v1.30.4)
- [SDESK-5021] Extend FTP transmit to push associations (superdesk/superdesk-client-core#3362)

### Superdesk Planning Change Log (v1.10.2-rc1)
- [SDESK-4863] Implement an Assignment Email layout that allows 'acceptance' of assignments (superdesk/superdesk-planning#1437)
- [SDESK-5010] Update allowed actions on pictures assignments in progress (superdesk/superdesk-planning#1429)

### Superdesk Analytics Change Log (v1.7.3)
- None

## [1.30.4] 2020-01-31
### AAP-Superdesk Changelog
- [SDESK-4847] Support downloading the MissionReport as CSV (#804)
- [SDESK-4775] Settings to add and map XMP files to picture coverages (#806)
- [SDESK-4776] Fulfill photo assignments from DC (#808)
- fix(vocabs): Fix missing comma in vocabs json data file (#813)
- [SDESK-4869] Update existing users user names (#810)
- [SDESK-4983] Indicate if a DC image has a high enough resolution to crop in Superdesk' (#815)
- [SDESK-4873] Ingest fuel prices from Petrol Spy (#800)
- [SDESK-4883] Require a macro to remove line breaks/pars and create run-on-text (#802)
- [SDESK-4867] Victorian harness racing macro (#805)
- fix(macro) vic harness racing macro fixes (#807)
- fix(racing macro) handle commas missing in selections (#812)
- fix(fuel macro) detect outlier values and remove old source (#811)
- [SDESK-4882] Collate golf results (#809)
- fix(fulfill assignment) set the poll frequency to every minute for the fulfill assignment task (#817)
- [SDESK-4903] Enable PLANNING_CHECK_FOR_ASSIGNMENT_ON_SEND setting (#818)
- [SDESK-4846] Add location notes to assignment emails (#797)
- fix(bom) retry download from BOM (#798)

### Superdesk-Core Change Log (v1.30.1)
- [SDESK-4869] Allow display_name to be formatted on ldap authentication (superdesk/superdesk-core#1782)
- [SDESK-4984] Empty error message on insufficient privileges to create a content template (superdesk/superdesk-core#1791)
- [SDESK-4901] Add anpa_take_key as 'Take Key' to fields available for content filters (superdesk/superdesk-core#1779)
- [SDESK-4368] In Newsroom, content item's publish schedule is not available (#1610)

### Superdesk-Client-Core Change Log (v1.30.4)
- [SDESK-4983] Make items with pubstatus withheld unfetchable (superdesk/superdesk-client-core#3325)
- [SDESK-4903] (1.30) Add 'authoring:send' functionPoint (superdesk/superdesk-client-core#3337)
- [SDESK-4913] Add Contact Type to search parameters in Contacts (superdesk/superdesk-client-core#3292)
- [SDESK-4984] Templates setings was accessible without content_templates privilege (superdesk/superdesk-client-core#3326)
- [SDESK-4697] Increase max results and sort ascending for 'Content Filter' dropdowns

### Superdesk Planning Change Log (v1.10.1)
#### Features
- [SDESK-4767] Feature to attach files to coverages (superdesk/superdesk-planning#1403)
- [SDESK-4775] Attach .xmp file to picture assignments (superdesk/superdesk-planning#1405)

#### Improvements
- [SDESK-4797] Reduce vertical padding in PopupEditor on small screens (superdesk/superdesk-planning#1402)
- fix: Automatically show contact popup when search text is empty (superdesk/superdesk-planning#1416)
- [SDESK-4979] Add coverage provider and assigned user names to coverages on posting the planning item (superdesk/superdesk-planning#1424)
- [SDESK-5001] Coverage Icons for graphic, video_explainer and live_blog (superdesk/superdesk-planning#1428)
- [SDESK-4903] (1.10) Show FulfilAssignment challenge on archive send (superdesk/superdesk-planning#1425)
- [SDESK-5022] Remove whitespace from the beginning and end of the name and slugline when saving an Event or Planning item and Coverages (superdesk/superdesk-planning#1432)

#### Fixes
- [SDESK-4889] Bug while removing an agenda (superdesk/superdesk-planning#1401)
- [SDESK-4929] Don't clear invalid date fields on autosave (superdesk/superdesk-planning#1406)
- [SDNTB-616] FIX: Update time is not working for ingested events. (superdesk/superdesk-planning#1404)
- [SDESK-4908] Paginate results in contacts selection in Event Form (superdesk/superdesk-planning#1407)
- [SDNTB-616] fix: update time not working for ingested events. (superdesk/superdesk-planning#1409)
- [sdesk-4776] Allow a user id to be passed to complete assignment (superdesk/superdesk-planning#1410)
- [SDESK-4509] Port e2e tests from Protractor to Cypress (superdesk/superdesk-planning#1408)
- [SDBELGA-262] (EVENT FILES) - Save additional file information. (superdesk/superdesk-planning#1412)
- fix(e2e): Failing to click on Contacts Close button (superdesk/superdesk-planning#1418)
- [SDESK-4888] Wrong history entry when creating a Planning item with a coverage (superdesk/superdesk-planning#1414)
- [SDESK-4890] Multiple errors when canceling a coverage (superdesk/superdesk-planning#1413)
- [SDESK-4976] Assignment notifications not having XMP file attachments (superdesk/superdesk-planning#1417)
- [SDESK-4796] Bug around assignment XMP mapping when XMP is attached during assignment creation (superdesk/superdesk-planning#1419)
- [SDNTB-622] (INGEST) NIFS event ingest parser error (superdesk/superdesk-planning#1415)
- [SDESK-4993] Planning item with an XMP file was not getting published (superdesk/superdesk-planning#1422)
- [SDESK-4977] Duplicating coverage or planning item should duplicate the XMP File too (superdesk/superdesk-planning#1423)
- [SDESK-4980] Create two locations with same name (superdesk/superdesk-planning#1420)
- [SDESK-4888] Wrong coverage history on creation (superdesk/superdesk-planning#1427)
- [SDESK-5004] Turning on the 'NOT FOR PUBLICATION' toggle enables the 'SAVE & POST' button in the Planning editor (superdesk/superdesk-planning#1426)
- [SDESK-5019] FIX: Add scrolling for coverage types list in add coverage advance mode. (superdesk/superdesk-planning#1430)
- [SDESK-5025] Related planning item(s) not published when event is cancelled (superdesk/superdesk-planning#1431)
- [SDESK-5030] Scheduled Update not in delivery record (superdesk/superdesk-planning#1433)
- fix(behave): Add privilege error message in expected response (superdesk/superdesk-planning#1435)

### Superdesk Analytics Change Log (v1.7.3)
- [SDESK-4847] Implement CSV download for tables (superdesk/superdesk-analytics#113)
- [SDESK-4695] Convert relative dates to absolute for date_histogram bounds (superdesk/superdesk-analytics#112)
- [SDESK-4695] (fix): Histogram aggregations failing for relative dates (superdesk/superdesk-analytics#114)
- fix(install): Fix installing mkdir for highcharts-export-server (superdesk/superdesk-analytics#115)
- fix(packages): Update versions based on GitHub recommendations (superdesk/superdesk-analytics#116)

## [1.30.3] 2019-12-12
### AAP-Superdesk Changelog
- [SDESK-4288] Format the image byline from DC (#792)
- [SDESK-4845] Make byline mandatory for images (#793)
- [SDESK-4848] Macro to retrieve weather data from the BOM (#794)

### Superdesk-Core Change Log (v1.30.1)
- [SDESK-4814] fix the feed query, request all versions, allow point in time recovery (superdesk/superdesk-core#1725)
- [SDESK-4766] Add 'contact_type' to Contacts resource (superdesk/superdesk-core#1727)
- [SDESK-4766] Data update for ContentType/CoverageProvider CVs (superdesk/superdesk-core#1745)

### Superdesk-Client-Core Change Log (v1.30.4)
- [SDESK-4766] Allow a Contact to have a 'contact_type' (superdesk/superdesk-client-core#3212)
- [SDESK-4766][SDESK-4857] Fix validation with Media Contact email (superdesk/superdesk-client-core#3238)

### Superdesk Planning Change Log (v1.10.0)
#### Features
- [SDESK-4766] Assign coverages to assignable media contacts (superdesk/superdesk-planning#1389)

#### Improvements
- [SDESK-4734] Confirmation on completing event (superdesk/superdesk-planning#1382)
- [SDESK-4721] Save location directly from location popup (superdesk/superdesk-planning#1386)
- [SDBELGA-220] improvements for quick creation of coverages (superdesk/superdesk-planning#1388) 
- [SDESK-4722] Add no result indication in location manager and set sort order on empty search (superdesk/superdesk-planning#1390)
- [SDESK-4807] Event templates privilege (superdesk/superdesk-planning#1394)
- [SDESK-4846] Add notes to locations (superdesk/superdesk-planning#1398)

#### Fixes
- [SDESK-4723] Improve stability when searching locations (superdesk/superdesk-planning#1384)
- [SDNTB-589] Use default timezone for rescheduling events if there is no timezone in event (superdesk/superdesk-planning#1385)
- [SDESK-4735] Infinite loading when unlocking an event thats being edited in popup (superdesk/superdesk-planning#1387)
- [SDESK-4389] Remove repeated 'by' in planning history tab (superdesk/superdesk-planning#1391)
- [SDESK-4772] Avoid planning lists' scroll position from jumping to start on item notifications (superdesk/superdesk-planning#1392)
- [SDESK-4806] Event templates were not saving 'category' field (superdesk/superdesk-planning#1393)
- [SDBELGA-220] validate coverage in add advanced modal (superdesk/superdesk-planning#1395)
- [SDESK-4766] Remove 'Start Working' for external coverages (superdesk/superdesk-planning#1397)
- [SDESK-4846] Styling changes to location details (superdesk/superdesk-planning#1399)
- [SDESK-4766] UX improvements for coverage provider contact (superdesk/superdesk-planning#1400)

## [1.30.2] 2019-11-06
### AAP-Superdesk Changelog
- [SDESK-4702] Update settings.py for base AAP settings (#784)
- [SDESK-4765] Add relay feeding service for AP images (#785)
- fix(abs macro) The ABS moved the token from the URL to the HTTP headers (#786)
- Revert "(fix): SMSReport tests failing due to Prague daylight savings" (#788)

### Superdesk-Core Change Log (v1.30.1)
- None

### Superdesk-Client-Core Change Log (v1.30.4)
#### Fixes
- [SDESK-4798] 'Associated as update' not prompting to link to scheduled_update (superdesk/superdesk-client-core#3190)

### Superdesk Planning Change Log (v1.9.0)
#### Features
- [SDESK-4560] Cherry-picking scheduled_updates feature to master (superdesk/superdesk-planning#1366)
  - [SDESK-4561] Coverage forward updates (superdesk/superdesk-planning#1293)
  - [SDESK-4647] Item actions for Scheduled Updates (superdesk/superdesk-planning#1316)
  - [SDESK-4562] Logically constrain the scheduling of planned updates to a coverage (superdesk/superdesk-planning#1324)
  - [SDESK-4563][SDESK-4564] Scheduled updates linking and unlinking features (superdesk/superdesk-planning#1332)
  - [SDESK-4727] Editor related bugs in Scheduled Updates creation (superdesk/superdesk-planning#1349)
  - [SDESK-4730] Changes to scheduled_updates feature and merging information to newsroom (superdesk/superdesk-planning#1353)
  - [SDESK-4758] Fixes to scheduled_updates feature (superdesk/superdesk-planning#1364)
  - [SDESK-4793] Removing assignment in a scheduled update chain should remove all assignments (superdesk/superdesk-planning#1376)

#### Improvements
- feat(dropdown): Improved behaviour for dropdown, added groups (superdesk/superdesk-planning#1361)
- [SDNTB-604] Move NTB related feed parser and formatter from planning to NTB repo (superdesk/superdesk-planning#1363)
- [SDBELGA-148] implement add coverages advanced modal (superdesk/superdesk-planning#1370)

#### Fixes
- [SDESK-4745] Correct the label for news value in planning preview (superdesk/superdesk-planning#1365)
- [SDESK-4771] Unable to change coverage schedule from 'To Be Confirmed' to default value (superdesk/superdesk-planning#1369)
- [SDESK-4774] Event links getting a null value when editing (superdesk/superdesk-planning#1368)
- [SDESK-4760] Planning Export dialog is showing all Agendas (superdesk/superdesk-planning#1372)
- [SDESK-4692] Posting a Planning item should post the entire series of Events (superdesk/superdesk-planning#1371)
- [SDBELGA-148] fix coverage duplication in advanced mode (superdesk/superdesk-planning#1374)
- [SDNTB-613] Fix buggy behaviour when trying to remove subjects from event and planning item (superdesk/superdesk-planning#1373)
- [SDESK-4714] Always open preview when clicking in-app Assignment notification (superdesk/superdesk-planning#1375)
- [SDESK-4692] (fix): Dont show PostEvent modal when saving Planning item (superdesk/superdesk-planning#1377)
- [SDESK-4741] Scroll issue in the Manage Events & Planning Filters window (superdesk/superdesk-planning#1378)
- [SDESK-4620] Display all affected Planning items when cancelling an Event (superdesk/superdesk-planning#1380)

### Superdesk Analytics Change Log (v1.7.2)
#### Improvements
- [SDESK-4779] Add subject to publishing based reports (superdesk/superdesk-analytics#111)

#### Fixes
- Set cores to Superdesk v1.30 (superdesk/superdesk-analytics#108)
- (fix): rewritten_by was not being cleared in stats (superdesk/superdesk-analytics#110)

## [1.30.1] 2019-10-17
### AAP-Superdesk Change Log
#### Features
- None

#### Improvements
- [SDESK-4756] Use browser time for 'events courts' template (#781)

#### Fixes
- fix(newsroom): GUIDs were published as the path to the file (#775)
- [SDESK-4752] Correct the filing date timezone (#779)

### Superdesk-Core Change Log (v1.30.1)
#### Feature
- None

#### Improvements
- [SDESK-4708] Create filter condition on on existence of featuremedia (superdesk/superdesk-core#1691)

### Fixes
- [SDESK-4728] Prevent out-of-sequence publishing of Updates (superdesk/superdesk-core#1681)

### Superdesk-Client-Core Change Log (v1.30.4)
#### Feature
- None

#### Improvements
- [SDESK-4708] Create filter condition on on existence of featuremedia (superdesk/superdesk-client-core#3152)

#### Fixes
- Node sass update, list item fix (superdesk/superdesk-client-core#3041)
- fix-e2e(1.30): Fix e2e tests webdriver updated (superdesk/superdesk-client-core#3133) (superdesk/superdesk-client-core#3148)
- fix(kill): Item schema not loading when killing from archived (superdesk/superdesk-client-core#3149)

### Superdesk Planning Change Log (v1.8.0)
#### Features
- [SDBELGA-101][SDBELGA-102][SDBELGA-103] Event templates (superdesk/superdesk-planning#1328)
- [SDESK-4565] Independently sort Assignment lists (superdesk/superdesk-planning#1344)
- [SDESK-4472] 'To be confirmed' feature (superdesk/superdesk-planning#1341)

#### Improvements
- [SDESK-4668] Introduce configuration for the main left hand side toolbar (superdesk/superdesk-planning#1336)
- [SDESK-4701] Align collapse box close button left and next to three-dot button (superdesk/superdesk-planning#1348)
- [SDBELGA-186] control via article template where generated content is inserted (superdesk/superdesk-planning#1354)
- [SDESK-4756] Provide browser time accesibility to events download templates (superdesk/superdesk-planning#1357)

#### Fixes
- [SDESK-4514] reopen editor if required when item is added to featured stories (superdesk/superdesk-planning#1331)
- [SDNTB-599] When duplicated event is rescheduled and posted, SD sends file with NTBID of orginal event (superdesk/superdesk-planning#1340)
- [SDESK-4515] Close editor after cancelling event/planning-item (superdesk/superdesk-planning#1342)
- [SDESK-4516] Event editor is blank when reducing repetitions if that event no longer exists (superdesk/superdesk-planning#1343)
- [SDESK-4515] Cancelling planning item was keeping the item in editor still locked (superdesk/superdesk-planning#1347)
- [SDESK-4663] The editor in 'Add To Planning' modal should close if the same Planning item is unlocked in another session (superdesk/superdesk-planning#1346)
- [SDESK-4710] Error when assigning past date to coverage (superdesk/superdesk-planning#1350)
- (fix) Place superdesk-core in peerDependencies and update Typescript version (superdesk/superdesk-planning#1351)
- [SDNTB-589] (fix): Cannot perform reschedule or convert to recurring on events. (superdesk/superdesk-planning#1352)
- fix duplicate by on slack notification (superdesk/superdesk-planning#1339)
- [SDESK-4757] 'Abstract' from news item was missing when planning item was exported as article (superdesk/superdesk-planning#1358)
- [SDESK-4648] User asked for saving changes when an event is not edited (superdesk/superdesk-planning#1359)


## [1.30] 2019-09-20
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
- fix(assignment templates) handle missing bits of address (#773)

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
- fix(auuthoring): Fixed issue with dropdown positions (superdesk-client-core#3056)

### Superdesk Planning Change Log (v1.7.0)
#### Features
- [SDESK-4427] New Event action 'Mark as Completed' (superdesk-planning#1273)
- [SDNTB-584] feat(draggable): Added ability to make modals draggable (superdesk-planning#1294)

#### Improvements
- [SDESK-4599] Review planning workflow notifications (superdesk-planning#1301)
- [SDESK-4598] Add Place to event and planning filter (superdesk-planning#1302)
- [SDESK-4618] Remove the folder from the filename returned for attachments (superdesk-planning#1307)
- [SDESK-4595] Move the attachment icon in lists (superdesk-planning#1311)
- [SDESK-4651] Show all desks by default in Fulfil Assignment modal (superdesk-planning#1305)
- [SDESK-4676] Hide 'all day' as an event form option (superdesk-planning#1320)
- [SDESK-4705] modify the internal note message (superdesk-planning#1334)

#### Fixes
- [SDESK-4427] Mark for complete fix to cater for events that start on same day but ahead in time. (superdesk-planning#1278)
- [SDESK-4592] Restrict some item actions on expired items (superdesk-planning#1297)
- actioned_date was removed when posting an event (superdesk-planning#1299)
- [SDESK-4224][SDESK-4510][SDESK-4513] (fix): Don't unmount the PopupEditor when action modal is shown (superdesk-planning#1274)
- [SDESK-4572] Don't close dropdown on scroll bar click (superdesk-planning#1303)
- [SDESK-4654] Handle the enter key in Selecting subject codes etc. (superdesk-planning#1312)
- [SDESK-4669] Location was getting deleted when event was marked as complete or assigned to calendar (superdesk-planning#1310)
- [SDESK-4661] (fix) Fulfil Assignment button visible if Assignment is locked (superdesk-planning#1306)
- (fix-requirements) Add responses lib in dev-requirements.txt (superdesk-planning#1315)
- [SDESK-4678] When marking an Event as completed Planning and Assignments need to be updated (superdesk-planning#1317)
- fix(flake8): Resolve 'D413 Missing blank line after last section' (superdesk-planning#1312)
- fix(import ui-framework): Add helpers and colors to scss imports (superdesk-planning#1323)
- fix to use modal__backdrop class locally (superdesk-planning#1326)
- [SDESK-4691] Planning was not published when event was completed (superdesk-planning#1330)
- fix(assignment templates) handle missing bits of address, add slugline to subject (superdesk-planning#1333)
- [SDESK-4704] Send Assignment notification when Event is updated (superdesk-planning#1337)
- [SDNTB-599] 'duplicate_from' was missing when duplicating an Event. (superdesk-planning#1335)


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

