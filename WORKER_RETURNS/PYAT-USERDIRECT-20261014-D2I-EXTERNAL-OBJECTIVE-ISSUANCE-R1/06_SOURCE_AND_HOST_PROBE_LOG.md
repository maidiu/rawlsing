# D2I — observed probes, not reconstructed binary custody

## Local host commands and outcomes

- python --version: Python 3.13.5.
- python -m pytest --version: pytest 9.0.2.
- git --version: git version 2.47.3.
- filesystem: write/read of /mnt/data/d2i_workspace/probe.txt PASS.
- Python requests HTTPS against www.google.com: ConnectionError / NameResolutionError, Temporary failure in name resolution (probe of general outbound DNS only).
- git ls-remote https://github.com/maidiu/rawlsing.git HEAD: exit 128; fatal unable to access remote, Could not resolve host: github.com. No authenticated Git checkout or owner-import regression claimed.
- container.download https://nca.org.gh/wp-content/uploads/2022/07/Q4-2021-statistical-Bulletin.pdf to /mnt/data/d2i_nca_q4_2021.pdf: ERROR download failed; no PDF created.
- GitHub connector fetch_file for sealed commission, D2F, N9C, SC0, OC05 and direct-producer module: PASS. Exact code owner blobs recorded in 00, 02, 03.
- Official GSS census2021 HTML report links to official report PDF; web open PDF 86 pages PASS, web screenshot PDF zero page 75 PASS (printed p. 62, rural lighting table visually clear).
- Alternative statsghana.gov.gh/gssmain/fileUpload/pressrelease/Volume%203K_Housing%20Characteristics_240222.pdf returned 404 via web; **not** evidence the actual census2021 publisher report vanished or changed.
- Official NCA publication page (8 Jul 2022) click through official PDF 36 pages PASS, text extract page 29 Table 10 and PDF page 10 definition of active mobile data PASS. NCA PDF screenshot page 29 repeated Cache miss / Internal Error. This does not negate independently readable official PDF table text.
- Raw official PDF binary length and SHA-256: NOT OBTAINED. Web PDF text extraction and page screenshot are not a byte-identical archive handoff. Official original-vs-current revision status and publisher records UNKNOWN.

## Actual test run

- cwd /mnt/data/d2i_workspace.
- python -m py_compile d2i_sourcefree.py: EXIT 0.
- python -m pytest -q --junitxml=pytest_receipt.xml: EXIT 0.
- stdout: ........................................ [100%] / 40 passed in 0.11s.
- JUnit locally generated at /mnt/data/d2i_workspace/pytest_receipt.xml (original local runtime copy; not uploaded as falsely reconstructed XML).
- Exact local git hash-object: module 0c902b55fed2508d3890e58e3ffae6b2237cd39b, test ee5dbb188aaad2a013225767fe66b1d8372e18ab, fixture d714ab12157e5d17e8e164c78b260743ebbe09d9. All three uploaded bytes independently match GitHub connector's returned blobs.
- No published PDF bytes staged to the test host, no live owner-import suite, no source-use/EE13/OC05 issuer invocation, no original respondent rows.
