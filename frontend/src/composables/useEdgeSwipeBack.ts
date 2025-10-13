// src/composables/useEdgeSwipeBack.ts
import {onMounted, onUnmounted} from 'vue'
import {useRouter} from 'vue-router'

interface SwipeBackOptions {
    minDx?: number
    maxDy?: number
    minVelocity?: number
}

function isInsideHorizontalScroller(element: HTMLElement | null): boolean {
    if (!element) return false
    let parent = element
    // Проверяем до 5 уровней вверх, этого обычно достаточно
    for (let i = 0; i < 5 && parent && parent !== document.body; i++) {
        const style = window.getComputedStyle(parent)
        const overflowX = style.getPropertyValue('overflow-x')
        const isScrollable = overflowX === 'auto' || overflowX === 'scroll'

        if (isScrollable && parent.scrollWidth > parent.clientWidth) {
            return true
        }
        parent = parent.parentElement as HTMLElement
    }
    return false
}


export function useEdgeSwipeBack(options: SwipeBackOptions = {}) {
    const router = useRouter()
    const {
        minDx = 80,
        maxDy = 120,
        minVelocity = 0.5  // px/ms
    } = options

    let startX = 0
    let startY = 0
    let startTime = 0
    let isTracking = false
    let isHorizontal: boolean | null = null

    const isSwipeDisabled = () => {
        return router.currentRoute.value.meta.disableSwipeBack === true
    }

    const handleTouchStart = (e: TouchEvent) => {
        if (isSwipeDisabled() || e.touches.length !== 1) return

        if (isInsideHorizontalScroller(e.target as HTMLElement)) {
            isTracking = false
            return;
        }

        startX = e.touches[0].clientX
        startY = e.touches[0].clientY
        startTime = Date.now()
        isTracking = true
        isHorizontal = null
    }

    const handleTouchMove = (e: TouchEvent) => {
        if (!isTracking || isSwipeDisabled()) return

        const currentX = e.touches[0].clientX
        const currentY = e.touches[0].clientY
        const deltaX = currentX - startX
        const deltaY = currentY - startY
        const absDeltaX = Math.abs(deltaX)
        const absDeltaY = Math.abs(deltaY)

        if (isHorizontal === null && (absDeltaX > 20 || absDeltaY > 20)) {
            isHorizontal = absDeltaX > absDeltaY * 1.5
        }

        if (isHorizontal && deltaX > 0) {
            if (absDeltaX > absDeltaY) {
                e.preventDefault()
            }

            if (absDeltaX >= minDx && absDeltaY <= maxDy) {
                console.log('🔙 Swipe back triggered!', {
                    deltaX: absDeltaX,
                    deltaY: absDeltaY
                })
                isTracking = false
                triggerNavigation()
            }
        } else if (isHorizontal === false) {
            isTracking = false
        }
    }

    const handleTouchEnd = (e: TouchEvent) => {
        if (!isTracking || isSwipeDisabled()) {
            isTracking = false
            return
        }

        const endX = e.changedTouches[0].clientX
        const endY = e.changedTouches[0].clientY
        const deltaX = endX - startX
        const deltaY = endY - startY
        const absDeltaX = Math.abs(deltaX)
        const absDeltaY = Math.abs(deltaY)
        const duration = Date.now() - startTime
        const velocity = absDeltaX / duration

        if (
            deltaX > 0 &&
            absDeltaX > absDeltaY * 1.5 &&
            velocity >= minVelocity &&
            absDeltaY <= maxDy &&
            duration < 500
        ) {
            console.log('⚡ Fast swipe detected!', {
                velocity: velocity.toFixed(2),
                duration
            })
            triggerNavigation()
        }

        isTracking = false
        isHorizontal = null
    }

    const triggerNavigation = () => {
        if (window.history.length > 1) {
            router.back()
        } else {
            window.Telegram?.WebApp?.close?.()
        }
    }

    onMounted(() => {
        document.addEventListener('touchstart', handleTouchStart, {passive: true})
        document.addEventListener('touchmove', handleTouchMove, {passive: false})
        document.addEventListener('touchend', handleTouchEnd, {passive: true})
    })

    onUnmounted(() => {
        document.removeEventListener('touchstart', handleTouchStart)
        document.removeEventListener('touchmove', handleTouchMove)
        document.removeEventListener('touchend', handleTouchEnd)
    })
}