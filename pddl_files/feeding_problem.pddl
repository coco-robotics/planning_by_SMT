(define (problem feeding_pb)
    (:domain feeding)

    (:objects spoon1 - spoon potato1 - potato mouth1 - location start_loc - location bowl1 - location)

    (:init (engaged spoon1 start_loc) (in potato1 bowl1) (unloaded spoon1)
    )

    (:goal (in potato1 mouth1))
)