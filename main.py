from builder.builder import Builder


aapl_data = Builder.build("AAPL", "01-01-2024", "03-01-2024", 0.5)

print(aapl_data.head())
