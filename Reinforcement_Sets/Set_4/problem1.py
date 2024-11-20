

class Locator:

    def _check_kind_body(self, srl: str)-> tuple[str,str]:
        'Checks if a valid kind and body were given'

        kind_body = srl.split(sep = ":")
        kind = kind_body[0]

        if any(char.isdigit() for char in kind):
            raise ValueError
            
        if not kind.islower() or len(kind_body) != 2:
            raise ValueError

        body = kind_body[1]
            
        if not body.startswith("//"):
            raise ValueError

        body = body[2:]

        if body.startswith(".") or body.endswith("."):
            raise ValueError

        return (kind, body)
    

    def _check_list_alnum(self, items: list[str])-> bool:
        'Checks if the iterable item has any none alpha-numeric character'

        for part in items:
            if not part.isalnum():
                return False

        return True


    def _check_location_resources(self, body: str)-> tuple[str, str]:
        'Checks if a valid location and resource were given'

        resources = ""

        location = ""

        if body.find("/") != -1:

            resources = body[body.find("/"):]

            resources_parts = resources.split(sep = "/")

            if not self._check_list_alnum(resources_parts) and resources_parts[0] != "":
                raise ValueError

            location = body[:body.find("/")]

        else:
            location = body

        return (location, resources)
        

    def __init__(self, srl: str):

        srl = srl.strip()

        try:
            kind, body = self._check_kind_body(srl)

            location, resources = self._check_location_resources(body)

            resources_parts = resources[1:].split(sep = "/")

            location_parts = location.split(sep = ".")

            if not self._check_list_alnum(location_parts):
                raise ValueError
            
        except ValueError:
            raise ValueError

        else:
            self._srl = srl
            self._kind = kind
            self._location = location
            self._location_parts = location_parts
            self._resources = resources
            self._resources_parts = resources_parts


    def kind(self)-> str:
        return self._kind

    def location(self)-> str:
        return self._location

    def location_parts(self) -> list[str]:
        return self._location_parts

    def resource(self)-> str:
        return self._resources

    def resource_parts(self)-> list[str]:
        return self._resources_parts

    def parent(self)-> 'Locator':
        if len(self.resource()) < 2:
            return Locator(f"{self.kind()}://{self.location()}{self.resource()}")
        else:
            new_resource = ""
            resource_parts = self.resource_parts()
            
            for index in range(len(resource_parts)-1):
                new_resource += f"/{resource_parts[index]}"

            new_locator = Locator(f"{self.kind()}://{self.location()}{new_resource}")
            return new_locator

    def within(self, resource_part: str)-> 'Locator':

        if not self._check_list_alnum(resource_part):
            raise ValueError

        return Locator(f"{self.kind()}://{self.location()}{self.resource()}/{resource_part}")

def _test_creation()-> None:
        
    x = Locator("https://chatgpt.com/")
    x = Locator("https://mail.google.com/mail/u/0/inbox")
    x = Locator("https://mail.google.com")

    words = ["https:/mail.google.com", "https://.mail.google.com",
             "https://mail.google.com.", "https:/4/mail.google.com", "",
             "https://mail.google.com?/mail/u/0/inbox"]

    for s in words:
        try:
            x = Locator(s)
        except ValueError:
            pass
        else:
            assert False


def _test_others()-> None:

    x = Locator("https://chatgpt.com/answer1/answer345/helloWorld")
    assert x.kind() == "https"
    assert x.location() == "chatgpt.com"
    assert x.location_parts() == ["chatgpt","com"]
    assert x.resource() == "/answer1/answer345/helloWorld"
    assert x.resource_parts() == ["answer1","answer345","helloWorld"]
    assert x.parent().resource() == Locator("https://chatgpt.com/answer1/answer345").resource()
    assert x.within("newPage123").resource() == Locator("https://chatgpt.com/answer1/answer345/helloWorld/newPage123").resource()

    try:
        x.within("newPa-ge123")
    except ValueError:
        pass
    else:
        assert False
    

if __name__ == "__main__":

    _test_creation()
    _test_others()

    



        







        
