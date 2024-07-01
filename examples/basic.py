import logging

from zambeze import Campaign, BasicActivity

def main():
    # Logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # Python methods to run as activities
    def reverse_words(line: str) -> str:
        return " ".join(reversed(line.split()))
    def count_words(line: str) -> int:
        return len(line.split())
    line_to_process = "Hello World"

    # Prepare activities
    rev_words_act = BasicActivity(
        "Reverse Words",
        reverse_words,
        line_to_process,
    )
    cnt_words_act = BasicActivity(
        name="Count Words",
        fn=count_words,
        line=line_to_process,
    )

    # Run campaign with the activities
    campaignExecutionResult = Campaign("Words Operations", logger=logger, 
                                             activities=[rev_words_act, cnt_words_act]).dispatch()
    for activityExecutionResult in campaignExecutionResult:
       logger.info(activityExecutionResult)


if __name__ == "__main__":
    main()