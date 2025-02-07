# Limit OSM data to just greater Vancouver
# Typical invocation:
# spark-submit just-vancouver.py amenities amenities-vancouver
# hdfs dfs -cat amenities-vancouver/* | gzip -d - | gzip -c > amenities-vancouver.json.gz

import sys
import logging  # Add this import

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark.sql import SparkSession, functions, types, Row
spark = SparkSession.builder.appName('OSM point of interest extracter').getOrCreate()
assert spark.version >= '2.4' # make sure we have Spark 2.4+
spark.sparkContext.setLogLevel('WARN')
#sc = spark.sparkContext


amenity_schema = types.StructType([
    types.StructField('lat', types.DoubleType(), nullable=False),
    types.StructField('lon', types.DoubleType(), nullable=False),
    types.StructField('timestamp', types.TimestampType(), nullable=False),
    types.StructField('amenity', types.StringType(), nullable=False),
    types.StructField('name', types.StringType(), nullable=True),
    types.StructField('tags', types.MapType(types.StringType(), types.StringType()), nullable=False),
])


def main(inputs, output):
    try:
        poi = spark.read.json(inputs, schema=amenity_schema)
        if poi.rdd.isEmpty():
            raise ValueError("Input data is empty or invalid.")

        poi = poi.filter((poi['lon'] > -123.5) & (poi['lon'] < -122))
        poi = poi.filter((poi['lat'] > 49) & (poi['lat'] < 49.5))

        if poi.rdd.isEmpty():
            raise ValueError("No data found within the specified Vancouver bounds.")

        poi.write.json(output, mode='overwrite', compression='gzip')
        logging.info(f"Data successfully written to {output}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == '__main__':
    inputs = sys.argv[1]
    output = sys.argv[2]
    main(inputs, output)
