from pyspark.sql import SparkSession

DATA_DIR = "../resources/data"
TEST_CASE_NAME = "PythonHdfsIn2HdfsOut1"

spark = SparkSession \
    .builder \
    .appName(TEST_CASE_NAME) \
    .enableHiveSupport() \
    .getOrCreate()

df1 = spark.read.option("header", "true").csv(DATA_DIR + "/in1.csv")
df2 = spark.read.option("header", "true").csv(DATA_DIR + "/in2.csv")
df1.createOrReplaceTempView("v1")
df2.createOrReplaceTempView("v2")

df = spark.sql("select v1.c1 as a, v1.c2 as b, v2.c1 as c, v2.c2 as d from v1 join v2 on v1.id = v2.id")

#InsertIntoHadoopFsRelationCommand
df.write.mode('overwrite').csv(DATA_DIR + "/" + TEST_CASE_NAME+"/out.csv")

spark.sparkContext.stop()

spark.stop()




