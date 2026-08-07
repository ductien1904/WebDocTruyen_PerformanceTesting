# PRD: Login

## 1. Objective

Allow a User who already has an account in the AMS (Account Management System) — Member, Manager, or Admin — to authenticate into the Training System from the public Home Page, so that role-specific features become available after sign-in.

Source: `Testing-System-SRS.docx`, section 4.2.1 "Login". Actors: Member, Manager, Admin (referred to collectively as "User" in the source spec).

## 2. Screen Layout (wireframe)

The source SRS references an embedded screenshot for the login form but does not include a labeled field-by-field mockup. The ASCII layout below is reconstructed from the field list and validation rules stated in section 4.2.1's Flow description; see the discrepancy note beneath it.

```
+---------------------------------------------+
|                  [ Logo ]                    |
|                                               |
|              Form đăng nhập                  |
|                                               |
|  Username                                    |
|  [__________________________________]       |
|                                               |
|  Password                                    |
|  [__________________________________]       |
|                                               |
|  [ ] Remember me                             |
|                                               |
|              [   Đăng nhập   ]               |
|                                               |
+---------------------------------------------+
```

**Discrepancies between mockup and field table:**
- The SRS does not state placeholder text for either field; the companion test-case spreadsheet (`VTI_Login_TestCase__1_.xlsx`, TC LP002/LP020) asserts a placeholder appears on blur-while-empty, but doesn't specify its literal text. Flagged in Open Questions.
- The SRS does not state whether the "Đăng nhập" (Login) button is ever disabled (e.g., while fields are empty); the mockup above assumes it is always enabled, consistent with the SRS's per-click validation model. Flagged in Open Questions.
- No error-message placement (inline vs. toast vs. modal) is defined in the SRS; the mockup omits it for that reason.

## 3. Field Definitions

| No. | Field (EN) | I/O | Format | Type | Required | Default | Min | Max | Placeholder | Allowed characters | Alignment |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Username | Input | Free text | Text box | Yes | Empty | 1 | 15 | Not specified in SRS (see Open Questions) | Not restricted in SRS; case- and diacritic-sensitive | Left |
| 2 | Password | Input | Free text, masked as `*` on screen | Text box (masked) | Yes | Empty | 1 | 25 | Not specified in SRS (see Open Questions) | Not restricted in SRS; case- and diacritic-sensitive | Left |
| 3 | Remember me | Input | N/A | Checkbox | No | Unchecked | N/A | N/A | N/A | N/A | Left |
| 4 | Đăng nhập (Login button) | Action | N/A | Button | N/A | Enabled | N/A | N/A | N/A | N/A | Center |

Notes:
- Min/Max for Username and Password are character-length bounds taken directly from the SRS Flow text: "ô input [User name] chỉ nhập được từ 1 ký tự → 15 ký tự" and "ô input [Password] chỉ nhập được từ 1 ký tự → 25 ký tự".
- The SRS explicitly calls out that Username and Password are case-sensitive and diacritic-sensitive ("phân biệt chữ hoa chữ thường, dấu").
- The SRS does not state a character allow-list (e.g., whether special characters are permitted) beyond the length bound — this is an Open Question.

## 4. Validation Rules & Error Messages

| No. | Field | Error case | Message shown (exact string) | Display style |
|---|---|---|---|---|
| 1 | Username | Empty, or length > 15 characters | `NDUY_09`: "User name không đúng định dạng" | Not specified in SRS (see Open Questions) |
| 2 | Password | Empty, or length > 25 characters | `NDUY_10`: "Password không đúng định dạng" | Not specified in SRS (see Open Questions) |
| 3 | Username + Password (combined) | Credentials do not match an account in AMS (includes wrong username, wrong password, or case mismatch, since both fields are case-sensitive) | `NDUY_11`: "User name và password không hợp lệ" | Not specified in SRS (see Open Questions) |

Additional behavior specified for the `NDUY_11` case: the system retains the Username value on screen and resets the Password field to empty.

Order of validation is not stated by the SRS (e.g., whether Username and Password format checks — `NDUY_09`/`NDUY_10` — both run before the AMS credential check `NDUY_11`, or whether the first failing rule short-circuits the rest). Flagged in Open Questions.

## 5. Success Flow

1. User is on the Home Page (not logged in) and clicks the "Đăng nhập" button, navigating to the Form đăng nhập screen.
2. User enters Username (1–15 characters) and Password (1–25 characters, displayed as `*`).
3. User optionally checks "Remember me".
4. User clicks the "Đăng nhập" button.
5. System validates Username and Password format (length/empty rules). If either fails, the corresponding error message (`NDUY_09` / `NDUY_10`) is shown and the flow stops.
6. If format validation passes, the system sends the credentials to AMS for authentication.
7. If AMS rejects the credentials, `NDUY_11` is shown, Username is retained, and Password is reset to empty.
8. If AMS accepts the credentials, the system navigates to the Home Page in a logged-in state, with the Role taken from the authenticated account.
9. On the Home Page header, the "Đăng nhập" button is replaced by the User's default avatar, the User's name, and a Logout control.
10. If "Remember me" was checked, the browser stores the Username and Password for the login form.

## 6. Open Questions

1. **Login button disabled state:** The SRS does not say whether the "Đăng nhập" button is ever disabled (e.g., while Username or Password is empty), or whether it is always clickable and relies entirely on post-click validation. Needs confirmation from BA/Dev.
2. **Placeholder text:** Neither field's placeholder string is defined in the SRS. The companion test-case spreadsheet assumes a placeholder appears on blur-while-empty but doesn't name the text.
3. **Allowed character set:** The SRS bounds Username/Password only by length; it does not say whether special characters (e.g., `@!#`) are permitted or rejected. The companion test-case spreadsheet flags this as unresolved.
4. **`maxlength` enforcement:** It's unspecified whether the 15/25-character bounds are enforced as an input-level `maxlength` (extra keystrokes silently dropped) or only checked on submit (allowing longer input to be typed and rejected via `NDUY_09`/`NDUY_10`). This changes whether "> max length" test cases are even reachable through the UI.
5. **Validation order:** Whether Username and Password format checks both run before the AMS check, or whether validation short-circuits on the first failure, is not stated.
6. **Error message display style:** Inline under the field, toast, or modal — not specified.
7. **"Remember me" unchecked behavior:** The SRS only describes what happens when the checkbox is checked (browser stores Username/Password). It does not state what happens on the next visit when it was left unchecked (e.g., whether any previously remembered value is cleared).
8. **Session persistence on browser Back:** Whether the logged-in state persists (or the login form re-appears) when the user presses the browser Back button after logging in is not addressed by the SRS.
9. **Network-loss handling:** The SRS does not define behavior if connectivity drops before, during, or after the login request (error message, timeout duration, retry behavior).
10. **"Dấu" (diacritics) sensitivity:** The SRS states Username/Password are sensitive to "chữ hoa chữ thường, dấu" (case and diacritics/tone marks) — worth confirming this literally means Vietnamese diacritic marks affect matching, since most system accounts are likely to be ASCII usernames.

## 7. Success Criteria

- A User with a valid AMS account can log in with correct Username/Password and reach the Home Page in a logged-in state with the correct Role.
- Username outside 1–15 characters (empty or too long) is rejected with `NDUY_09`, and the form remains on the login screen.
- Password outside 1–25 characters (empty or too long) is rejected with `NDUY_10`, and the form remains on the login screen.
- Any Username/Password combination that AMS does not recognize (including a case-mismatched but otherwise correct pair) is rejected with `NDUY_11`, Username is retained, and Password is reset to empty.
- Checking "Remember me" before a successful login causes the browser to retain Username and Password for a subsequent visit to the login form.
- Password characters are always rendered as `*` on screen, regardless of entry method (typing, paste, autofill).
