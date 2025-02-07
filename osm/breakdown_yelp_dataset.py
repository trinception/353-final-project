# Yelp business dataset retrieved from https://www.kaggle.com/yelp-dataset/yelp-dataset/version/3?select=yelp_academic_dataset_business.json
import sys
import pandas as pd
import numpy as np
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

# from pyspark.sql import SparkSession, functions, types, Row
# spark = SparkSession.builder.appName('Extract Vancouver reviews from Yelp dataset').getOrCreate()
# assert spark.version >= '2.4' # make sure we have Spark 2.4+
# spark.sparkContext.setLogLevel('WARN')
# #sc = spark.sparkContext
#
#
# business_schema = types.StructType([
#     types.StructField('business_id', types.StringType()),
#     types.StructField('name', types.StringType()),
#     types.StructField('address', types.StringType()),
#     types.StructField('city', types.StringType()),
#     types.StructField('state', types.StringType()),
#     types.StructField('postal_code', types.StringType()),
#     types.StructField('latitude', types.FloatType()),
#     types.StructField('longitude', types.FloatType()),
#     types.StructField('stars', types.FloatType()),
#     types.StructField('review_count', types.LongType()),
#     types.StructField('is_open', types.LongType()),
#     types.StructField('attributes', types.MapType(types.StringType(), types.StringType()), nullable=False),
#     types.StructField('categories', types.StringType()),
#     types.StructField('hours', types.MapType(types.StringType(), types.StringType()), nullable=False),
# ])

def main(inputs):
    # business = spark.read.json(inputs, schema=business_schema)
    # vancouver = business.filter((business['city']== 'Vancouver') & (business['state']=='BC') & (business['is_open']==1))
    # vancouver_ratings=vancouver.select(
    #     'name', 'address', 'latitude', 'longitude', 'stars','review_count', 'hours'
    # )
    # #return vancouver_ratings
    # #vancouver.show()
    # #vancouver_ratings.show()
    #
    # vancouver_ratings.write.json("amenities_rated", mode='overwrite')

     business = pd.read_json(inputs, lines= True)
     business['latitude']= pd.to_numeric(business['latitude'], errors='coerce')
     business['longitude']= pd.to_numeric(business['longitude'], errors='coerce')
     business['stars']= pd.to_numeric(business['stars'], errors='coerce')
     business['review_count']= pd.to_numeric(business['review_count'], errors='coerce')

     vancouver = business[business['city']=='Vancouver']# & business['state']=='BC'& business['is_open']==1]
     BC = vancouver[vancouver['state']=='BC']
     open = BC[BC['is_open']==1]
     # open['lat']= open['latitude']
     # open['lon']= open['longitude']

     vancouver_ratings = open.drop(['business_id', 'city','state', 'postal_code','latitude','longitude','is_open','attributes','categories'], axis=1)
     vancouver_ratings['lat']=open['latitude']
     vancouver_ratings['lon']=open['longitude']
     #print(vancouver_ratings)
     vancouver_ratings.to_json("rated_amenities.json")

if __name__ == '__main__':
    inputs = sys.argv[1]
    main(inputs)
