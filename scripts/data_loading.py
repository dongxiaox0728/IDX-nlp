import os
import mysql.connector
import pandas as pd


def get_connection():

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "root"),
        database=os.getenv("MYSQL_DATABASE", "real_estate"),
    )


def load_listing_sample(limit=1000):

    conn = get_connection()

    query = f"""
        SELECT 
            L_ListingID,
            L_Address,
            L_City,
            L_Keyword2 AS beds,
            LM_Dec_3 AS baths,
            L_SystemPrice AS price,
            L_Remarks AS remarks
        FROM rets_property
        WHERE L_Remarks IS NOT NULL
          AND LENGTH(L_Remarks) > 50
        ORDER BY RAND()
        LIMIT {limit};
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df


def main():
    output_dir = "data/processed"
    output_file = os.path.join(output_dir, "listing_sample.csv")

    os.makedirs(output_dir, exist_ok=True)

    print("Connecting to MySQL and loading listing sample...")

    df = load_listing_sample(limit=1000)

    df.to_csv(output_file, index=False)

    print(f"Saved {len(df)} rows to {output_file}")


if __name__ == "__main__":
    main()