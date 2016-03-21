def sweet_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    print("firstName = " + event['firstName'])
    print("lastName = " + event['lastName'])
    return event['firstName']  # Echo back the first key value
    #raise Exception('Something went wrong')
