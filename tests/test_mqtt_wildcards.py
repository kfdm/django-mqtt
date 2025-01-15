from dmqtt.signals import convert_wildcards

def test_convert_wildcards():
    # Test basic wildcard conversion
    assert convert_wildcards("home/#") == "home/*"
    assert convert_wildcards("home/+/temp") == "home/?/temp"
    
    # Test multiple wildcards
    assert convert_wildcards("home/#/+/test") == "home/*/?/test"
    
    # Test no wildcards
    assert convert_wildcards("home/kitchen/temp") == "home/kitchen/temp"
    
    # Test empty string
    assert convert_wildcards("") == ""
    
    # Test mixed wildcards
    assert convert_wildcards("#/+/#/+") == "*/?/*/?"