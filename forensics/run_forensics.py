from .forensic_reader import load_latest, render_report
from .feature_extractors import extract_features


def main():
    run = load_latest()

    if not run:
        print("No data available.")
        return

    features = extract_features(run)
    report = render_report(features)

    print(report)


if __name__ == "__main__":
    main()
