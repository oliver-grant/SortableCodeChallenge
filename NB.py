import json
import io
import re

Products        = [] # full products as a list of dictionaries
Result          = [] # final result objects
Product_H_Space = [] # product names (split) with hyphens converted to spaces
Product_No_H    = [] # product names (split) with hyphens removed
# Read in the products
with open('products.txt') as f:
    for line in f:
        product = json.loads(line)
        Products.append(product)
        Result.append({"product_name": product["product_name"], "listings": []})
        Product_H_Space.append(set(re.split('_|-', product["product_name"].upper())))
        Product_No_H.append(set(re.split('_', re.sub('-', '', product["product_name"].upper()))))


# Reads in listings file. For each listing, it goes through all products and
# adds its listing to the first product it "mathes". A "match" ifor a listing
# is defined as containing at least |name of product|-1 of the words in the
# name of the product, and somewhere contains the same manufacturer, family
# (if available) and model.
num_matches = 0
with open('listings.txt', encoding="utf8") as f:
    i = 0
    for line in f:
        listing = json.loads(line)
        listing_h_space = set(re.split(' |-', listing["title"].upper()))
        listing_no_h = set(re.split(' ', re.sub('-()', '', listing["title"].upper())))
        listing_both_h = listing_h_space | listing_no_h 
        product_count = 0
        for product in Products:
            if (((len(Product_H_Space[product_count] & listing_both_h)
            >= (len(Product_H_Space[product_count]) -1)) or 
            (len(Product_No_H[product_count] &
            listing_both_h) >=
            (len(Product_No_H[product_count]) -1))) and
            (product["manufacturer"].upper() in
            listing["manufacturer"].upper().split(' ')) and
            (not("family" in product) or (re.sub('-| ', '',
            product["family"].upper()) in listing_both_h)) and
            (re.sub('-| ', '', product["model"].upper()) in
            listing_both_h)):
                Result[product_count]["listings"].append(listing)
                num_matches = num_matches + 1
                break
            product_count = product_count + 1


# Print out the results
print(num_matches)
f = io.open("Results.txt", 'w', encoding='utf8')         
for r in Result:
    f.write(json.dumps(r))
    f.write('\n')
