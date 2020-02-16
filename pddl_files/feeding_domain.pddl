(define (domain feeding)
    (:requirements :strips :typing)
    (:types spoon potato location)

    (:predicates (engaged ?sp - spoon ?l - location)
                 (loaded ?sp - spoon)
                 (unloaded ?sp - spoon)
                 (in ?p -potato ?l - location)
    )

    (:action engage
        :parameters (?sp - spoon ?from ?to - location)
        :precondition (and (engaged ?sp ?from))
        :effect (and (engaged ?sp ?to) (not (engaged ?sp ?from)))
    )

    (:action load
        :parameters (?sp - spoon ?p - potato ?l - location)
        :precondition (and (unloaded ?sp) (engaged ?sp ?l) (in ?p ?l))
        :effect (and (loaded ?sp) (not (unloaded ?sp)) (not (in ?p ?l)))
    )

    (:action unload
        :parameters (?sp - spoon ?p - potato ?l - location)
        :precondition (and (loaded ?sp) (engaged ?sp ?l))
        :effect (and (unloaded ?sp) (not (loaded ?sp)) (in ?p ?l))
    )
)