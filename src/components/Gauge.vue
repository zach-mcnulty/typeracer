<script setup lang="ts">
  import { useTemplateRef, onMounted, watch } from 'vue'

  const props = withDefaults(defineProps<{ value: number}>(), { value: 0 })

  const canvas = useTemplateRef('canvas')

  let gauge;

  watch(() => props.value, (value) => {
    gauge && gauge.set(Math.min(value, 120))
  })

  onMounted(() => {
    var opts = {
      angle: -0.25, // The span of the gauge arc
      lineWidth: 0.25, // The line thickness
      radiusScale: 0.75, // Relative radius
      pointer: {
        length: 0.75, // // Relative to gauge radius
        strokeWidth: 0.035, // The thickness
        color: '#a00' // Fill color
      },
      limitMax: false,     // If false, max value increases automatically if value > maxValue
      limitMin: false,     // If true, the min value of the gauge will be fixed
      colorStart: '#6FADCF',   // Colors
      colorStop: '#8FC0DA',    // just experiment with them
      strokeColor: '#E0E0E0',  // to see which ones work best for you
      generateGradient: true,
      highDpiSupport: true,     // High resolution support
      renderTicks: {
        divisions: 12,
        divWidth: 1.1,
        divLength: 0.7,
        divColor: "#333333",
        subDivisions: 2,
        subLength: 0.5,
        subWidth: 0.6,
        subColor: "#666666"
      },
      staticLabels: {
        font: "10px sans-serif",
        labels: [
          {label:10},
          {label:20},
          {label:30},
          {label:40},
          {label:50},
          {label:60},
          {label:70},
          {label:80},
          {label:90},
          {label:100},
          {label:110},
          {label:120},
        ],
        fractionDigits: 0
      },
      staticZones: [
        {strokeStyle: "#ccc", min: 0, max: 100},
        {strokeStyle: "#f00", min: 100, max: 120},
      ],
    };

    gauge = new Gauge(canvas.value).setOptions(opts); // create sexy gauge!
    gauge.maxValue = 120; // set max gauge value
    gauge.setMinValue(0);  // Prefer setter over gauge.minValue = 0
    gauge.animationSpeed = 32; // set animation speed (32 is default value)
    gauge.set(0);
  })
</script>

<template>
  <div class="relative w-[380px]">
    <div class="text-center absolute w-full top-28 text-xl font-bold">
      {{ value.toFixed(0) }}
    </div>
    <canvas ref="canvas" width="380" height="150"></canvas>
  </div>
</template>