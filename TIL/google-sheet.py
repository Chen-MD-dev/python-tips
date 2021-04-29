from __future__ import print_function
import pickle
import os.path
import pandas as pd
import urllib
import pymssql
import sqlalchemy
import urllib.parse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from sqlalchemy import create_engine

# google sheet api : https://developers.google.com/sheets/api/quickstart/python
# google sheet api key : https://cloud.google.com/docs/authentication/api-keys

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1111"
SAMPLE_RANGE_NAME = "백엔드연동(수정금지)!A4:E"


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
		# access api key
    import httplib2
    service = build("sheets", "v4", http=httplib2.Http(), developerKey="AAAAA")

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])

    if not values:
        print("No data found.")
    else:
        keyword_data = get_kewords()
        """
        google sheet row 순서
        0. 부가서비스
        1. 업체 장점 한마디
        2. 업체 하고싶은말
        3. 타입폼 이미지 Url
        4. 업체 id
        """
        for row in values:
            try:
                user_name = row[4]
                user_pic = row[3]
                row.append(user_pic)
                # keyword from mssql
                user_keyword = keyword_data.get(user_name, "")
                row.append(user_keyword)
            except:
                pass
        df = pd.DataFrame(
            values,
            columns=[
                "addition",
                "title",
                "description",
                "_",
                "adminid",
                "profile_img",
                "keyword",
            ],
        )
        # mssql db insert
        server = "url"
        database = "db_name"
        username = "admin"
        password = "admin"
        params = urllib.parse.quote_plus(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            + "SERVER="
            + server
            + ";DATABASE="
            + database
            + ";UID="
            + username
            + ";PWD="
            + password
        )
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
        df.to_sql(
            "partner_metadata",
            con=engine,
            if_exists="replace",
            index=True,
            index_label="id",
            dtype={
                "adminid": sqlalchemy.types.VARCHAR(length=25),
                "title": sqlalchemy.types.VARCHAR(length=255),
                "keyword": sqlalchemy.types.VARCHAR(length=255),
                "profile_img": sqlalchemy.types.VARCHAR(length=255),
                "addition": sqlalchemy.types.VARCHAR(),
                "description": sqlalchemy.types.VARCHAR(),
            },
        )

def get_kewords():
    conn = pymssql.connect(
        server="url",
        user="admin",
        password="admin",
        database="db_name",
        charset="utf8"
    )
    curs = conn.cursor(as_dict=True)
    sql = "select adminid, keyword from partner_metadata"
    curs.execute(sql)
    rows = curs.fetchall()
    ret_dict = {}
    for row in rows:
        ret_dict[row["adminid"]] = row["keyword"]
    conn.close()
    return ret_dict


if __name__ == "__main__":
    main()
