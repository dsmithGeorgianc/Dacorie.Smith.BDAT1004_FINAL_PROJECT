import requests


class ReCaptchaVerifier:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.verification_url = "https://www.google.com/recaptcha/api/siteverify"

    def verify(self, response, remote_ip=None):
        """
        Verifies the reCAPTCHA response with Google's reCAPTCHA API.

        Parameters:
        - response (str): The user response token provided by the reCAPTCHA on your site.
        - remote_ip (str, optional): The user's IP address.

        Returns:
        - dict: A dictionary with the API response.
        """

        payload = {
            "secret": self.secret_key,
            "response": response
        }

        if remote_ip:
            payload["remoteip"] = remote_ip

        result = requests.post(self.verification_url, data=payload)

        return result.json()


# Example usage:
#recaptcha_verifier = ReCaptchaVerifier(secret_key="YOUR_SECRET_KEY_HERE")
#verification_result = recaptcha_verifier.verify(response="03ADUVZwAcL1TD6uXuGq5AhnbC3HVqiNOH2XtG5pud4tIRDfZhoJrbFYMpe3ZWaFHWcoSqGjuT8HQ8nMt11bhrJwH2_X6nz9lovK7WtXTKi4TlTnLocNaJtO0ua8VwrpS_IGKtHFutMrChke40mbF6ZGEfwJKwP387SDwZy0zIGb_DCjB3InssakoclBi5ya6x59Td4JJn7Iw178_Zw0DEgSooNZh_e-OXNrAuVcE2lFYC8B2HDAYugboENExJQP92rhzszUDCzfcd_ULnhQfzVAXp09Alqg9co95q48tsYuEZtyTZWbsZNWtzD8ZV7csJ9U34wItI4x4OkWjY5oYYVubpC1gEYsL9skdr_d041u2rjojL8yG3RTYwgCTqip_8NdUQsrXR8wy2aqWIyPlaB7zjwIMMjzFxzeXn9upA54wH1uR1-MsDXpe-r7fJNGL7xxwvq41minwKDtge_seA8qMBywdsMGolg0wtoNsqrsLyMGgKBx-LqGeAS9_VzlVfywZ3SL8CLQBsPj1sUvfm8kQNqy1mSJL8yYtonWx-2zd_URZWQlVc3iq90kKF3Tfqh6o8LOmfI1JGJ3H2muLWfvv_I_mZwwMRTDPmWC4QUhBT9_iLH0HoMBZuIngn0hAlzPUAZ1RNNI-rzJhZ7FB6mFwQu69AizwB8XQRYjZfwNFXEDsyXO6cpTXDPXi4gmGMg7KxWo1XRZ-SUwvvK604JbsjFioFzmtIzUw6bZwp0h2V0nOgr1BiH79LIhsBFbFQpGPcbPO10cr0jQEY45Do9Z9HsvtITJpA7tjOIfMy4xTxthf9P_gyfZ-ZSAzHDAf0HHciQllPC2KD9TX-3j70ClPj3dIcQJEbtZDaQZ8oO70mL0wTpfRsN8K_hc2sxSZqpzquCM31LrGZdBPbNP8iK6VZ-lKeNE6L00pNWxzMvZuUsMEPSNtNNXAl-4cL9wx_L0WjCP8lu7NMXgWu0U0AxObJSMFSfvLYmN0WGspsEwmwGUBQKNY2I7nZmuSI3WcfTj9uWdvJOdbXi0wvmtgNSiARvwmcAgVnpYIxkBfjvsWePU0fvB-ig83LnnFBXUXAp4RoKUkhshGtwrqYSG0y7VjfWDTD5_Jrq1R86ocfRLfgs0WZP20xyQ_vYn51ElZE-7xNvow3tW8zsNqklNGH2IBz4Ipcr6qZeViJfYT9QJ7oowW5JbKa-BK1bRvAEAno4EoGKVpVKprdQh4i3UJk4CwGXFIgBUNyDLP1deynyzq08q_B8CYTtO5g3ysmtHwVN-OPiw4afiwTYRNbP1XPUcOd5ry0FYYhN33m_uzdXPzrxeIg3SmxTBe273mvWzKaUbUXe_WU-xUBlEbaooOae1yAjDV6iy8JbXzfjyjTIHqjVeFoqDptUWlcBuUcSmz226gSGt-LQtTKvJ2LopLmEPLWNZzALKnlmNjooVv7tkmnXx2OkPcey4-WgwMHtsD9SJYVBDL5knFwMWMERj_39aksOLqqRu6sK4mPWnlG7Gf6YuYw3AwkNwAu6yZmgKFyxcbA5sH0_MW7",
#                                               remote_ip="USER_IP_ADDRESS_HERE")  # IP is optional
#print(verification_result)
