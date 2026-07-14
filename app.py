import streamlit as st

st.set_page_config(
    page_title="Matrix Chain Multiplication",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Matrix Chain Multiplication using Dynamic Programming")

st.write("""
This application computes:

- Minimum number of scalar multiplications
- Optimal Parenthesization
- Dynamic Programming Cost Table

**Time Complexity:** O(n³)

**Space Complexity:** O(n²)
""")


# ---------------- Matrix Chain Multiplication ----------------

def matrix_chain_order(dims):

    n = len(dims) - 1

    m = [[0]*(n+1) for _ in range(n+1)]
    s = [[0]*(n+1) for _ in range(n+1)]

    for l in range(2, n+1):

        for i in range(1, n-l+2):

            j = i + l - 1

            m[i][j] = float("inf")

            for k in range(i, j):

                cost = (
                    m[i][k]
                    + m[k+1][j]
                    + dims[i-1] * dims[k] * dims[j]
                )

                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k

    return m, s


def print_optimal_parens(s, i, j):

    if i == j:
        return f"A{i}"

    k = s[i][j]

    left = print_optimal_parens(s, i, k)
    right = print_optimal_parens(s, k+1, j)

    return f"({left} × {right})"


# ---------------- Sidebar ----------------

st.sidebar.header("Input")

default = "10,30,5,60,10"

dim_text = st.sidebar.text_input(
    "Enter Dimensions",
    value=default
)

run = st.sidebar.button("Compute")


# ---------------- Main ----------------

if run:

    try:

        dims = [int(x.strip()) for x in dim_text.split(",")]

        if len(dims) < 2:
            st.error("Enter at least two dimensions.")
            st.stop()

        n = len(dims)-1

        st.subheader("Matrices")

        for i in range(n):
            st.write(f"**A{i+1}** : {dims[i]} × {dims[i+1]}")

        m, s = matrix_chain_order(dims)

        st.success(f"Minimum Scalar Multiplications = {m[1][n]}")

        st.info(
            "Optimal Parenthesization: "
            + print_optimal_parens(s,1,n)
        )

        st.subheader("DP Cost Table")

        table=[]

        header=[""]+[f"A{i}" for i in range(1,n+1)]

        table.append(header)

        for i in range(1,n+1):

            row=[f"A{i}"]

            for j in range(1,n+1):

                if j<i:
                    row.append("---")
                else:
                    row.append(m[i][j])

            table.append(row)

        st.table(table)

    except:

        st.error("Please enter valid comma-separated integers.")
