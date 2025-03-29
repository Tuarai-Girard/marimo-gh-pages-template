import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _():
    from simple_salesforce import Salesforce
    import pandas as pd
    return Salesforce, pd


@app.cell
def _(Salesforce, logging, os):
    def connect_to_salesforce():
        """Connects to Salesforce using environment variables.

        Returns:
            Salesforce: An authenticated Salesforce connection object.

        Raises:
            Exception: If the connection fails.
        """
        try:
            sf = Salesforce(
                username=os.getenv('SF_USERNAME'),
                password=os.getenv('SF_PASSWORD'),
                security_token=os.getenv('SF_SECURITY_TOKEN')
            )
            logging.info("Connected to Salesforce successfully.")
            return sf
        except Exception as e:
            logging.error(f"Error connecting to Salesforce: {e}")
            raise   
    return (connect_to_salesforce,)


@app.cell
def _(connect_to_salesforce):
    sf = connect_to_salesforce()
    return (sf,)


@app.cell
def _(pd, sf):
    user_df = pd.json_normalize(
        sf.query_all('''
            SELECT Id, FirstName, LastName, Title, UserRole.Name
            FROM User
            WHERE isActive = True
            ORDER BY UserRole.Name, Title, Name
        ''')['records']
    )

    user_df = user_df.drop(columns=[col for col in user_df.columns if 'attributes' in col])
    return (user_df,)


@app.cell
def _(user_df):
    user_df
    return


if __name__ == "__main__":
    app.run()
