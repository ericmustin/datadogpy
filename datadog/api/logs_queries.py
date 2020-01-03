from datadog.api.resources import ActionAPIResource

class LogsQueries(ActionAPIResource):
    """
    A wrapper around LogsQueries HTTP API.
    """
    _resource_name = 'logs-queries'

    @classmethod
    def list(cls, **body):
        """
        Retrieve a list of logs

        :returns: Dictionary representing the API's JSON response
        """

        return super(LogsQueries, cls)._trigger_class_action('POST', 'list', **body)

    @classmethod
    def list_all(cls, **body):
        """
        Retrieve a list of paginated logs

        :returns: Array representing the API's JSON response concatenated together
        """

        request_body = body
        storage = []
        previous_id = 0

        if "startAt" not in request_body:
            request_body["startAt"] = None

        while previous_id != request_body["startAt"]:
            previous_id = request_body["startAt"]
            result = super(LogsQueries, cls)._trigger_class_action('POST', 'list', **request_body)

            if len(result["logs"]) == 0:
                break

            if "nextLogId" in result:
                request_body["startAt"] = result["nextLogId"]
            else:
                request_body["startAt"] = None
            
            storage = storage + result["logs"]

            if request_body["startAt"] is None:
                break

        return storage
