Feature: Content Auto Publishing
    @auth
    Scenario: Publish a user content using macro
      Given the "validators"
      """
        [
        {
            "schema": {},
            "type": "text",
            "act": "publish",
            "_id": "publish_text"
        },
        {
            "schema": {},
            "type": "text",
            "act": "auto_publish",
            "_id": "auto_publish_text"
        },
        {
            "_id": "publish_composite",
            "act": "publish",
            "type": "composite",
            "schema": {}
        }
        ]
      """
      And "desks"
      """
      [{"name": "Sports", "content_expiry": 60}]
      """
      When we post to "/archive" with success
      """
      [{"guid": "123", "type": "text", "headline": "test", "state": "fetched",
        "task": {"desk": "#desks._id#", "stage": "#desks.incoming_stage#", "user": "#CONTEXT_USER_ID#"},
        "subject":[{"qcode": "17004000", "name": "Statistics"}],
        "slugline": "test",
        "body_html": "Test Document body"}]
      """
      Then we get OK response
      And we get existing resource
      """
      {"_current_version": 1, "state": "fetched", "task":{"desk": "#desks._id#", "stage": "#desks.incoming_stage#"}}
      """
      When we post to "/products" with success
      """
      {
        "name":"prod-1","codes":"abc,xyz", "product_type": "both"
      }
      """
      And we post to "/subscribers" with "digital" and success
      """
      {
        "name":"Channel 1","media_type":"media", "subscriber_type": "digital", "sequence_num_settings":{"min" : 1, "max" : 10}, "email": "test@test.com",
        "products": ["#products._id#"],
        "destinations":[{"name":"Test","format": "nitf", "delivery_type":"email","config":{"recipients":"test@test.com"}}]
      }
      """
      And we post to "/subscribers" with "wire" and success
      """
      {
        "name":"Channel 2","media_type":"media", "subscriber_type": "wire", "sequence_num_settings":{"min" : 1, "max" : 10}, "email": "test@test.com",
        "products": ["#products._id#"],
        "destinations":[{"name":"Test","format": "nitf", "delivery_type":"email","config":{"recipients":"test@test.com"}}]
      }
      """
      When we post to "/macros"
      """
      {
        "macro": "Auto Publish", "item": {"_id": "#archive._id#"}
      }
      """
      Then we get OK response
      When we get "/published"
      Then we get existing resource
      """
      {"_items" : [{"_id": "123", "guid": "123", "headline": "test", "_current_version": 2, "state": "published",
        "task": {"desk": "#desks._id#", "stage": "#desks.incoming_stage#", "user": "#CONTEXT_USER_ID#"}}]}
      """
      When we get "/legal_archive"
      Then we get existing resource
      """
      {"_items" : [
        {"_id": "123", "guid": "123", "headline": "test", "_current_version": 2, "state": "published",
         "task": {"desk": "Sports", "stage": "Incoming Stage", "user": "test_user"},
         "slugline": "test",
         "body_html": "Test Document body", "subject":[{"qcode": "17004000", "name": "Statistics"}]}
        ]
      }
      """
      When we get "/legal_archive/123?version=all"
      Then we get list with 2 items
      """
      {"_items" : [
        {"_id": "123", "headline": "test", "_current_version": 1, "state": "fetched",
         "task": {"desk": "Sports", "stage": "Incoming Stage", "user": "test_user"}},
        {"_id": "123", "headline": "test", "_current_version": 2, "state": "published",
         "task": {"desk": "Sports", "stage": "Incoming Stage", "user": "test_user"}}
       ]
      }
      """
      When we enqueue published
      When we get "/publish_queue"
      Then we get list with 2 items
      """
      {
        "_items": [
          {"state": "pending", "content_type": "text",
          "subscriber_id": "#wire#", "item_id": "123", "item_version": 2},
          {"state": "pending", "content_type": "text",
          "subscriber_id": "#digital#", "item_id": "123", "item_version": 2}
        ]
      }
      """
      When run import legal publish queue
      When we enqueue published
      And we get "/legal_publish_queue"
      Then we get list with 0 items
